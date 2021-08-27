#!/usr/bin/env python3
import abc
import argparse
import json
import os
import sys
from os import path

if os.getenv("PIPELINE_EXECUTOR") is not None and os.getenv("PIPELINE_EXECUTOR") == "SLURM":
    file_dir = path.dirname(os.path.realpath(__file__))
    pipeline_dir = path.dirname(file_dir)
    sys.path.append(pipeline_dir)

from af.pipeline.db import services as db_services
from af.pipeline.db.core import DBConfig
from af.pipeline import config
from pydantic import ValidationError
from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.exceptions import InvalidAnalysisRequest


class Analyze(abc.ABC):

    @abc.abstractmethod
    def pre_process(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def analyze(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def run_job(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def post_process(self, *args, **kwargs):
        pass

    @abc.abctractmethod
    def process_job_result(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_engine_script(self):
        pass


def get_analyze_object(analysis_request: AnalysisRequest, session=None):
    """Returns the configured Analyze object based on engine name"""
    if not session:
        session = DBConfig.get_session()

    analysis_engine_meta = db_services.get_analysis_config_meta_data(
        session, analysis_request.analysisConfigPropertyId, "engine"
    )

    kls = config.get_analyze_class(analysis_engine_meta.value)
    return kls(analysis_request, engine_script=config._script(analysis_engine_meta.value))


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



