#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from os import path

if os.getenv("PIPELINE_EXECUTOR") is not None and os.getenv("PIPELINE_EXECUTOR") == "SLURM":
    file_dir = path.dirname(os.path.realpath(__file__))
    pipeline_dir = path.dirname(file_dir)
    sys.path.append(pipeline_dir)

from af.pipeline import config, dpo, utils
from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.db import services as db_services
from af.pipeline.db.core import DBConfig
from af.pipeline.db.models import Analysis, Job
from af.pipeline.exceptions import AnalysisError, DpoException, InvalidAnalysisRequest


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

        # Create DB record for Analysis

        # Add new analysis
        self.analysis = Analysis(
            request_id=self._analysis_request.id,
            name=analysis_request.requestId,
            creation_timestamp=datetime.utcnow(),
            status="IN-PROGRESS",  # TODO: Find, What this status and how they are defined
        )

        self.analysis = db_services.add(self.db_session, self.analysis)

        self.output_file_path = path.join(analysis_request.outputFolder, "result.zip")

    def pre_process(self):

        # Run data pre-processing to get asreml job file and processed data files.
        job_name = f"{self.analysis_request.requestId}-dpo"
        job_status = "IN-PROGRESS"
        status_message = "Running Data Pre-Processing."

        job = self.__get_new_job(job_name, job_status, status_message)

        try:
            job_input_files = dpo.ProcessData(self.analysis_request).run()
            return job_input_files
        except (DataReaderException, DpoException) as e:
            self.analysis.status = "FAILED"
            self.__update_job(job, "FAILED", str(e))
            raise AnalysisError(str(e))
        finally:
            self.db_session.commit()

    def analyze(self, job_input_files):
        """Takes a list of analysis job objects and run analysis for each.
        example:
            [
                {
                    "job_name": "job1"
                    "data_file": "/test/test.csv",
                    "asreml_job_file": "/test/test.as"
                }
            ]
        Returns:
            List of job output object with below fields,
            [
                {
                    "job_name": "job1",
                    "job_result_dir": "/test/"
                }
            ]
        """
        analysis_engine_meta = db_services.get_analysis_config_meta_data(
            self.db_session, self.analysis_request.analysisConfigPropertyId, "engine"
        )

        analysis_engine = config.get_analysis_engine_script(analysis_engine_meta.value)

        # output of each analysis job
        job_results = []

        for job_input_file in job_input_files:

            job_name = job_input_file["job_name"]
            asreml_job_file = job_input_file["asreml_job_file"]
            data_file = job_input_file["data_file"]

            job_status = "IN-PROGRESS"
            status_message = "Processing the input request"

            job = self.__get_new_job(job_name, job_status, status_message)

            try:

                cmd = [analysis_engine, asreml_job_file, data_file]

                run_result = subprocess.run(cmd, capture_output=True)

                job_status = utils.get_job_status(run_result.stdout, run_result.stderr)

                if job_status > 100:
                    status_message = run_result.stdout.decode("utf-8")[:50]

                job = self.__update_job(job, job_status, status_message)

                job_results.append({"job_name": job_name, "job_result_dir": utils.get_parent_dir(data_file)})

            except Exception as e:
                self.analysis.status = "FAILED"
                self.__update_job(job, "FAILED", str(e))
                raise AnalysisError(str(e))
            finally:
                self.db_session.commit()

        self.analysis.status = "COMPLETED"
        self.analysis.modification_timestamp = datetime.utcnow()
        self.db_session.commit()

        return job_results

    def post_process(self, job_results):

        for job_result in job_results:

            utils.zip_dir(job_result["job_result_dir"], self.output_file_path, job_result["job_name"])

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
        # TODO: 50 char limit in database for status messages need to be removed.
        job.status_message = status_message[:50]
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
