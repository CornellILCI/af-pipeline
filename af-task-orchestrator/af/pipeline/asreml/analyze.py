import os
import subprocess
import sys
from datetime import datetime
from os import path

import pandas as pd

if os.getenv("PIPELINE_EXECUTOR") is not None and os.getenv("PIPELINE_EXECUTOR") == "SLURM":
    file_dir = path.dirname(os.path.realpath(__file__))
    pipeline_dir = path.dirname(file_dir)
    sys.path.append(pipeline_dir)

from af.pipeline import analysis_report, calculation_engine, utils
from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.analyze import Analyze
from af.pipeline.asreml import services as asreml_services
from af.pipeline.asreml.dpo import AsremlProcessData
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.db import services as db_services
from af.pipeline.db.core import DBConfig
from af.pipeline.exceptions import AnalysisError, DpoException
from af.pipeline.job_data import JobData
from af.pipeline.job_status import JobStatus


class AsremlAnalyze(Analyze):

    dpo_cls = AsremlProcessData
    engine_script = "asreml"

    def __init__(self, analysis_request: AnalysisRequest, *args, **kwargs):
        super().__init__(analysis_request=analysis_request, *args, **kwargs)

        self.output_file_path = path.join(analysis_request.outputFolder, "result.zip")
        self.report_file_path = path.join(analysis_request.outputFolder, f"{analysis_request.requestId}_report.xlsx")
        # the engine script would have been determined from get_analyze_object so just pass it here

    def pre_process(self):

        self._update_request_status("IN-PROGRESS", "Data preprocessing in progress")

        try:
            job_input_files = self.get_process_data(self.analysis_request).run()
            self._update_request_status("IN-PROGRESS", "Data preprocessing completed. Running jobs.")
            return job_input_files
        except (DataReaderException, DpoException) as e:
            self.__update_request_status("FAILURE", "Data preprocessing failed.")
            utils.zip_dir(self.analysis_request.outputFolder, self.output_file_path)
            raise AnalysisError(str(e))
        finally:
            self.db_session.commit()

    def __update_request_status(self, status, message):
        self.analysis.request.status = status
        self.analysis.request.msg = message

    def get_engine_script(self):
        return self.engine_script

    def run_job(self, job_data, analysis_engine=None):

        if not analysis_engine:
            analysis_engine = self.get_engine_script()

        job_dir = utils.get_parent_dir(job_data.data_file)

        job_detail = {
            "trait_name": job_data.trait_name,
            "location_name": job_data.location_name,
        }

        job = db_services.create_job(
            self.db_session,
            self.analysis.id,
            job_data.job_name,
            JobStatus.INPROGRESS,
            "Processing in the input request",
            job_detail,
        )

        try:
            cmd = [analysis_engine, job_data.job_file, job_data.data_file]
            _ = subprocess.run(cmd, capture_output=True)
            job = db_services.update_job(
                self.db_session, job, JobStatus.INPROGRESS, "Completed the job. Pending post processing."
            )

            job_data.job_result_dir = job_dir

            return job_data
        except Exception as e:
            self.analysis.status = "FAILURE"
            db_services.update_job(self.db_session, job, JobStatus.ERROR, str(e))
            utils.zip_dir(job_dir, self.output_file_path, job_data.job_name)
            raise AnalysisError(str(e))
        finally:
            self.db_session.commit()

    def process_job_result(self, job_result: JobData, gathered_objects: dict = None):
        try:

            job = db_services.get_job_by_name(self.db_session, job_result.job_name)
            asr_file_path = path.join(job_result.job_result_dir, f"{job.name}.asr")

            exptloc_analysis_pattern = db_services.get_property(
                self.db_session, self.analysis_request.expLocAnalysisPatternPropertyId
            )

            if not path.exists(asr_file_path):
                raise AnalysisError("Analysis result asr file not found.")

            # parse predictions, model stats from xml and save to db
            asreml_result_xml_path = path.join(job_result.job_result_dir, f"{job.name}.xml")
            asreml_result_content = asreml_services.process_asreml_result(
                self.db_session, job.id, asreml_result_xml_path
            )

            if not asreml_result_content.model_stat.get("is_converged"):
                db_services.update_job(
                    self.db_session,
                    job,
                    JobStatus.FAILED,
                    asreml_result_content.model_stat.get("conclusion"),
                )
                return gathered_objects

            metadata_df = utils.get_metadata(job_result.metadata_file)

            # initialize the report workbook
            if not os.path.isfile(self.report_file_path):
                utils.create_workbook(self.report_file_path, sheet_names=analysis_report.REPORT_SHEETS)

            predictions_df = pd.DataFrame(asreml_result_content.predictions)

            # write prediction to the analysis report
            analysis_report.write_predictions(
                self.db_session,
                self.analysis_request,
                self.report_file_path,
                predictions_df,
                metadata_df,
            )

            if exptloc_analysis_pattern.code == "SESL":
                # get h2 cullis
                h2_cullis = None

                # get average standard error
                pvs_file_path = path.join(job_result.job_result_dir, f"{job.name}_pvs.txt")
                avg_std_error = asreml_services.get_average_std_error(pvs_file_path)

                entry_variances = db_services.query_variance(self.db_session, job.id, "entry")

                if len(entry_variances) == 1:
                    genetic_variance = entry_variances[0].component

                    try:
                        h2_cullis = calculation_engine.get_h2_cullis(genetic_variance, avg_std_error)

                        # round h2 cullis to 4 decimal points
                        h2_cullis = round(h2_cullis, 4)
                    except ValueError as ve:
                        h2_cullis = str(ve)

            # write model statisics to analysis report
            rename_keys = {"log_lik": "LogL"}
            analysis_report.write_model_stat(
                self.report_file_path, asreml_result_content.model_stat, metadata_df, rename_keys, h2_cullis=h2_cullis
            )

            # parse yhat result and save to db
            yhat_file_path = path.join(job_result.job_result_dir, f"{job.name}_yht.txt")
            if not path.exists(yhat_file_path):
                raise AnalysisError("Analysis result yhat file not found.")
            asreml_services.process_yhat_result(self.db_session, job.id, yhat_file_path)

            db_services.update_job(
                self.db_session, job, JobStatus.FINISHED, asreml_result_content.model_stat.get("conclusion")
            )

            # gather occurrences from the jobs, so we don't have to read occurrences again.
            # will not work for parallel jobs. For parallel job, gather will happen in finalize
            if "occurrences" not in gathered_objects:
                gathered_objects["occurrences"] = {}

            for occurrence in job_result.occurrences:
                if occurrence.occurrence_id not in gathered_objects["occurrences"]:
                    gathered_objects["occurrences"][occurrence.occurrence_id] = occurrence

            return gathered_objects

        except Exception as e:
            self.analysis.status = "FAILURE"
            db_services.update_job(self.db_session, job, JobStatus.ERROR, str(e))
            raise AnalysisError(str(e))
        finally:
            # zip the result files to be downloaded by the users
            utils.zip_dir(job_result.job_result_dir, self.output_file_path, job.name)

            self.db_session.commit()

    def finalize(self, gathered_objects):
        """
        tasks to run finally after all process done
        """

        if os.path.isfile(self.report_file_path):

            analysis_report.write_request_settings(self.db_session, self.report_file_path, self.analysis_request)

            if "occurrences" in gathered_objects:
                analysis_report.write_occurrences(self.report_file_path, gathered_objects["occurrences"])

            utils.remove_empty_worksheets(self.report_file_path)

            utils.zip_file(self.report_file_path, self.output_file_path)
        else:
            raise AnalysisError("No analysis result report generated by the engine. Analysis failed.")