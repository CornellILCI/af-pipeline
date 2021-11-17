#!/usr/bin/env python3
import abc
import argparse
import datetime
import json
import os
import sys
from os import path

from af.pipeline.db.models import Analysis, Job

if os.getenv("PIPELINE_EXECUTOR") is not None and os.getenv("PIPELINE_EXECUTOR") == "SLURM":
    file_dir = path.dirname(os.path.realpath(__file__))
    pipeline_dir = path.dirname(file_dir)
    sys.path.append(pipeline_dir)

from af.pipeline import config
from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.db import services as db_services
from af.pipeline.db.core import DBConfig
from af.pipeline.dpo import ProcessData
from af.pipeline.exceptions import InvalidAnalysisRequest
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



    def get_process_data(self, analysis_request, *args, **kwargs):
        """Get the associated ProcessData object for this Analyze"""
        return self.dpo_cls(analysis_request)

    @abc.abstractmethod
    def pre_process(self, *args, **kwargs):
        """Do pre-processing of data needed for analysis.  The list of input files
        should be returned by this method.

        TODO:  Assess other analysis (sommeR) if this really needs to be abstract.
    
        """
        pass

    @abc.abstractmethod
    def run_job(self, job_input_file, *args, **kwargs):
        """
        This method should define the execution of the job given the input_file.
        """
        pass

    @abc.abstractmethod
    def process_job_result(self, *args, **kwargs):
        """
        This method should define the processing of the job_result of a given job.
        """
        pass

    # @abc.abstractmethod
    # def run(self, *args, **kwargs):
    #     pass  TODO:  maybe this should be a concrete run()

    def get_engine_script(self):
        return self.engine_script
        
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


def get_analyze_object(analysis_request: AnalysisRequest, session=None):
    """Returns the configured Analyze object based on engine name"""
    if not session:
        session = DBConfig.get_session()

    analysis_engine_meta = db_services.get_analysis_config_meta_data(
        session, analysis_request.analysisConfigPropertyId, "engine"
    )

    kls = config.get_analyze_class(analysis_engine_meta.value)
    return kls(analysis_request, engine_script=config.get_analysis_engine_script(analysis_engine_meta.value))


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