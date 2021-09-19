#!/usr/bin/env python3

import argparse
import json
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

from af.pipeline import analysis_report, config, dpo, pandasutil, utils
from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.asreml import services as asreml_services
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.db import services as db_services
from af.pipeline.db.core import DBConfig
from af.pipeline.db.models import Analysis, Job
from af.pipeline.exceptions import AnalysisError, DpoException, InvalidAnalysisRequest
from af.pipeline.job_data import JobData
from pydantic import ValidationError


class Analyze:
    def __init__(self, analysis_request: AnalysisRequest):
        """Constructor.

        Constructs analysis db record and other required objects.

        Args:
            analysis_request: Object with all required inputs to run analysis.
        """

        self.analysis_request = analysis_request

        self.db_session = DBConfig.get_session()

        # Request source, DB record
        self._analysis_request = db_services.get_request(self.db_session, analysis_request.requestId)

        # load existing analysis record OR create if it does not exist
        self.analysis = db_services.get_analysis_by_request_and_name(
            self.db_session, request_id=self._analysis_request.id, name=analysis_request.requestId
        )

        if not self.analysis:
            # Create DB record for Analysis
            self.analysis = Analysis(
                request_id=self._analysis_request.id,
                name=analysis_request.requestId,
                creation_timestamp=datetime.utcnow(),
                status="IN-PROGRESS",  # TODO: Find, What this status and how they are defined
            )

            self.analysis = db_services.add(self.db_session, self.analysis)

        self.output_file_path = path.join(analysis_request.outputFolder, "result.zip")
        self.report_file_path = path.join(analysis_request.outputFolder, "report.xlsx")

    def pre_process(self):

        # Run data pre-processing to get asreml job file and processed data files.
        job_name = f"{self.analysis_request.requestId}-dpo"
        job_status = "IN-PROGRESS"
        status_message = "Running Data Pre-Processing."

        job = self.__get_new_job(job_name, job_status, status_message)

        try:
            job_data = dpo.ProcessData(self.analysis_request).run()
            self.__update_job(job, "IN-PROGRESS", "Data Pre-Processing completed.")
            return job_data
        except (DataReaderException, DpoException) as e:
            self.analysis.status = "FAILED"
            self.__update_job(job, "FAILED", "Failed during Data Pre-Processing.")
            raise AnalysisError(str(e))
        finally:
            self.db_session.commit()

    def analyze(self, jobs_to_run):
        """Takes a list of analysis job objects and run analysis for each.
        example:
            [
                {
                    "job_name": "job1"
                    "data_file": "/test/test.csv",
                    "job_file": "/test/test.as",
                    "metadata_file": "/test/test_metadata.csv"
                }
            ]
        Returns:
            List of job output object with below fields,
            [
                {
                    "job_name": "job1",
                    "job_id": "jobId1",
                    "job_result_dir": "/test/",
                    "data_file": "/test/test.csv",
                    "job_file": "/test/test.as",
                    "metadata_file": "/test/test_metadata.csv"
                }
            ]
        """

        # output of each analysis job
        job_results = []

        for job_data in jobs_to_run:
            job_result = self.run_job(job_data, self.get_engine())
            job_results.append(job_result)

        self.analysis.status = "COMPLETED"
        self.analysis.modification_timestamp = datetime.utcnow()
        self.db_session.commit()

        return job_results

    def get_engine(self):
        analysis_engine_meta = db_services.get_analysis_config_meta_data(
            self.db_session, self.analysis_request.analysisConfigPropertyId, "engine"
        )

        return config.get_analysis_engine_script(analysis_engine_meta.value)

    def run_job(self, job_data, analysis_engine):

        job_data = JobData(**job_data)

        job_name = job_data.job_name
        asreml_job_file = job_data.job_file
        data_file = job_data.data_file
        job_dir = utils.get_parent_dir(data_file)

        job_status = "IN-PROGRESS"
        status_message = "Processing the input request"

        job = self.__get_new_job(job_name, job_status, status_message)

        try:
            cmd = [analysis_engine, asreml_job_file, data_file]
            _ = subprocess.run(cmd, capture_output=True)
            job = self.__update_job(job, "COMPLETED", "Completed the job.")

            job_data.job_result_dir = job_dir

            return job_data

        except Exception as e:
            self.analysis.status = "FAILED"
            self.__update_job(job, "FAILED", str(e))
            raise AnalysisError(str(e))
        finally:
            self.db_session.commit()

    def post_process(self, job_results):
        for job_result in job_results:
            self.process_job_result(job_result)

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
            utils.create_workbook(self.report_file_path, sheet_names=analysis_report.REPORT_SHEETS)

            # write prediction to the analysis report
            analysis_report.write_predictions(self.report_file_path, asreml_result_content.predictions, metadata_df)

            # write model statisics to analysis report
            analysis_report.write_model_stat(self.report_file_path, asreml_result_content.model_stat, metadata_df)

            # parse yhat result and save to db
            yhat_file_path = path.join(job_result.job_result_dir, f"{job.name}_yht.txt")
            if not path.exists(yhat_file_path):
                raise AnalysisError("Analysis result yhat file not found.")
            asreml_services.process_yhat_result(self.db_session, job.id, yhat_file_path)

            # zip the result files to be downloaded by the users
            utils.zip_dir(job_result.job_result_dir, self.output_file_path, job.name)

            self.__update_job(job, "SUCCESS", "Asreml analysis completed successfully")

            # gather occurrences from the jobs, so we don't have to read occurrences again.
            # will not work for parallel jobs. For parallel job, gather will happen in finalize
            if "occurrences" not in gathered_objects:
                gathered_objects["occurrences"] = {}

            for occurrence in job_result.occurrences:
                if occurrence.occurrence_id not in gathered_objects["occurrences"]:
                    gathered_objects["occurrences"][occurrence.occurrence_id] = occurrence

            return gathered_objects

        except Exception as e:
            self.analysis.status = "FAILED"
            self.__update_job(job, "FAILED", str(e))
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

    def __get_new_job(self, job_name: str, status: str, status_message: str) -> Job:

        job_start_time = datetime.utcnow()
        job = Job(
            analysis_id=self.analysis.id,
            name=job_name,
            time_start=job_start_time,
            creation_timestamp=job_start_time,
            status=status,
            status_message=status_message,
        )

        job = db_services.add(self.db_session, job)

        return job

    def __update_job(self, job: Job, status: str, status_message: str):

        job.status = status
        job.status_message = status_message
        job.time_end = datetime.utcnow()
        job.modification_timestamp = datetime.utcnow()

        return job

    def run(self):
        """Runs the phenotypic analysis for given request.

        Pre process requested data using dpo module and run analysis engine with the job file and data file.
        Save the status of the analysis to the database.

        Returns:
            exit code 0 if sucessful. -1 if fialed
        """

        analysis_input_files = self.pre_process()

        analysis_results = self.analyze(analysis_input_files)

        self.post_process(analysis_results)

        return 0


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process input data to feed into analytical engine")

    parser.add_argument("--request_file", help="File path for analysis request")

    args = parser.parse_args()

    if path.exists(args.request_file):
        with open(args.request_file) as f:
            try:
                analysis_request: AnalysisRequest = AnalysisRequest(**json.load(f))
            except ValidationError as e:
                raise InvalidAnalysisRequest(str(e))
    else:
        raise InvalidAnalysisRequest(f"Request file {args.request_file} not found")

    sys.exit(Analyze(analysis_request).run())
