#!/usr/bin/env python3
import abc
import argparse
import datetime
import json
import os
import subprocess
import sys
from os import path

from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.db.models import Analysis, Job

if os.getenv("PIPELINE_EXECUTOR") is not None and os.getenv("PIPELINE_EXECUTOR") == "SLURM":
    file_dir = path.dirname(os.path.realpath(__file__))
    pipeline_dir = path.dirname(file_dir)
    sys.path.append(pipeline_dir)

from af.pipeline import config, utils
from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.db import services as db_services
from af.pipeline.db.core import DBConfig
from af.pipeline.dpo import ProcessData
from af.pipeline.job_status import JobStatus
from af.pipeline.exceptions import AnalysisError, DpoException, InvalidAnalysisRequest
from pydantic import ValidationError


class Analyze(abc.ABC):

    dpo_cls: ProcessData = None
    engine_script: str = ""

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
        self.report_file_path = path.join(analysis_request.outputFolder, f"{analysis_request.requestId}_report.xlsx")

    def get_process_data(self, analysis_request, *args, **kwargs):
        """Get the associated ProcessData object for this Analyze"""
        return self.dpo_cls(analysis_request)

    @abc.abstractmethod
    def pre_process(self):
        status = "IN-PROGRESS"
        message = "Data preprocessing in progress"
        try:
            job_input_files = self.get_process_data(self.analysis_request).run()
            message = "Data preprocessing completed. Running jobs."
            return job_input_files
        except (DataReaderException, DpoException) as e:
            status = "FAILURE"
            message = "Data preprocessing failed."
            raise AnalysisError(str(e))
        finally:
            self._update_request_status(status, message)
            self.db_session.commit()

    def _update_request_status(self, status, message):
        self.analysis.request.status = status
        self.analysis.request.msg = message

    def get_engine_script(self):
        return self.engine_script

    def get_cmd(self, job_data, analysis_engine=None):
        if not analysis_engine:
            analysis_engine = self.get_engine_script()
        return [analysis_engine, job_data.job_file, job_data.data_file]

    @abc.abstractmethod
    def run_job(self, job_data, analysis_engine=None):
        job_dir = utils.get_parent_dir(job_data.data_file)

        job = db_services.create_job(
            self.db_session, self.analysis.id, job_data.job_name, "IN-PROGRESS", "Processing in the input request"
        )

        try:
            cmd = self.get_cmd(job_data, analysis_engine)
            _ = subprocess.run(cmd, capture_output=True)
            job = db_services.update_job(
                self.db_session, job, "IN-PROGRESS", "Completed the job. Pending post processing."
            )

            job_data.job_result_dir = job_dir

            return job_data
        except Exception as e:
            self.analysis.status = "FAILURE"
            db_services.update_job(self.db_session, job, "FAILURE", str(e))
            raise AnalysisError(str(e))
        finally:
            self.db_session.commit()

    @abc.abstractmethod
    def process_job_result(self, *args, **kwargs):
        """
        This method should define the processing of the job_result of a given job.
        """
        pass

    def _get_new_job(self, job_name: str, status: str, status_message: str) -> Job:

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

    def _update_job(self, job: Job, status: str, status_message: str):

        job.status = status
        job.status_message = status_message
        job.time_end = datetime.utcnow()
        job.modification_timestamp = datetime.utcnow()

        return job

    def _update_request_status(self, status, message):
        self.analysis.request.status = status
        self.analysis.request.msg = message

    def _raise_job_error(self, job, e):
        self.analysis.status = "FAILURE"
        db_services.update_job(self.db_session, job, JobStatus.ERROR, str(e))
        utils.zip_dir(job_dir, self.output_file_path, job.name)
        raise AnalysisError(str(e))


def get_analyze_object(analysis_request: AnalysisRequest, session=None):
    """Returns the configured Analyze object based on engine name"""
    if not session:
        session = DBConfig.get_session()

    analysis_engine_meta = db_services.get_analysis_config_meta_data(
        session, analysis_request.analysisConfigPropertyId, "engine"
    )
    engine_script = config.get_analysis_engine_script(analysis_engine_meta.value)
    kls = config.get_analyze_class(engine_script)
    return kls(analysis_request, engine_script=engine_script)


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

    sys.exit(get_analyze_object(analysis_request).run())
