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

from af.pipeline import analysis_report, utils
from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.analyze import Analyze
from af.pipeline.asreml import services as asreml_services
from af.pipeline.asreml.dpo import AsremlProcessData
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.db import services as db_services
from af.pipeline.db.core import DBConfig
from af.pipeline.exceptions import AnalysisError, DpoException
from af.pipeline.job_data import JobData


class AsremlAnalyze(Analyze):

    dpo_cls = AsremlProcessData
    engine_script = "asreml"

    def __init__(self, analysis_request: AnalysisRequest, *args, **kwargs):
        """Constructor.

        Constructs analysis db record and other required objects.

        Args:
            analysis_request: Object with all required inputs to run analysis.
        """

        self.analysis_request = analysis_request

        self.db_session = DBConfig.get_session()

        # load existing analysis record OR create if it does not exist
        self.analysis = db_services.get_analysis_by_request_id(self.db_session, request_id=analysis_request.requestId)

        self.output_file_path = path.join(analysis_request.outputFolder, "result.zip")
        self.report_file_path = path.join(analysis_request.outputFolder, "report.xlsx")
        # the engine script would have been determined from get_analyze_object so just pass it here

    def pre_process(self):

        self.__update_request_status("IN-PROGRESS", "Data preprocessing in progress")

        try:
            job_input_files = self.get_process_data(self.analysis_request).run()
            self.__update_request_status("IN-PROGRESS", "Data preprocessing completed. Running jobs.")
            return job_input_files
        except (DataReaderException, DpoException) as e:
            self.__update_request_status("FAILURE", "Data preprocessing failed.")
            raise AnalysisError(str(e))
        finally:
            self.db_session.commit()

    def __update_request_status(self, status, message):
        self.analysis.request.status = "IN-PROGRESS"
        self.analysis.request.msg = message

    def get_engine_script(self):
        return self.engine_script

    def run_job(self, job_data, analysis_engine=None):

        if not analysis_engine:
            analysis_engine = self.get_engine_script()

        job_dir = utils.get_parent_dir(job_data.data_file)

        job = db_services.create_job(
            self.db_session, self.analysis.id, job_data.job_name, "IN-PROGRESS", "Processing in the input request"
        )

        try:
            cmd = [analysis_engine, job_data.job_file, job_data.data_file]
            _ = subprocess.run(cmd, capture_output=True)
            job = db_services.update_job(
                self.db_session, job, "IN-PROGRESS", "Completed the job. Pending post processing."
            )

            job_data.job_result_dir = job_dir

            return job_data
        except Exception as e:
            self.analysis.status = "FAILURE"
            db_services.update_job(self.db_session, job, "ERROR", str(e))
            raise AnalysisError(str(e))
        finally:
            self.db_session.commit()

    def process_job_result(self, job_result: JobData, gathered_objects: dict = None):
        try:

            job = db_services.get_job_by_name(self.db_session, job_result.job_name)
            asr_file_path = path.join(job_result.job_result_dir, f"{job.name}.asr")

            if not path.exists(asr_file_path):
                raise AnalysisError("Analysis result asr file not found.")

            # parse predictions, model stats from xml and save to db
            asreml_result_xml_path = path.join(job_result.job_result_dir, f"{job.name}.xml")
            asreml_result_content = asreml_services.process_asreml_result(
                self.db_session, job.id, asreml_result_xml_path
            )

            metadata_df = pd.read_csv(job_result.metadata_file, sep="\t", dtype=str)

            # initialize the report workbook
            if not os.path.isfile(self.report_file_path):
                utils.create_workbook(self.report_file_path, sheet_names=analysis_report.REPORT_SHEETS)

            # write prediction to the analysis report
            analysis_report.write_predictions(self.report_file_path, asreml_result_content.predictions, metadata_df)

            # write model statisics to analysis report
            rename_keys = {"log_lik": "LogL"}
            analysis_report.write_model_stat(
                self.report_file_path, asreml_result_content.model_stat, metadata_df, rename_keys
            )

            # parse yhat result and save to db
            yhat_file_path = path.join(job_result.job_result_dir, f"{job.name}_yht.txt")
            if not path.exists(yhat_file_path):
                raise AnalysisError("Analysis result yhat file not found.")
            asreml_services.process_yhat_result(self.db_session, job.id, yhat_file_path)

            # zip the result files to be downloaded by the users
            utils.zip_dir(job_result.job_result_dir, self.output_file_path, job.name)

            db_services.update_job(self.db_session, job, "DONE", "Asreml analysis completed successfully")

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
            db_services.update_job(self.db_session, job, "ERROR", str(e))
            raise AnalysisError(str(e))
        finally:
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
