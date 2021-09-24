#!/usr/bin/env python3

import argparse
import json
import os

# import pathlib
import sys
from abc import ABC, abstractmethod

# from collections import OrderedDict
from os import path

from pydantic import ValidationError

if os.getenv("PIPELINE_EXECUTOR") is not None and os.getenv("PIPELINE_EXECUTOR") == "SLURM":
    file_dir = path.dirname(os.path.realpath(__file__))
    pipeline_dir = path.dirname(file_dir)
    sys.path.append(pipeline_dir)

# from af.pipeline import config
from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.exceptions import InvalidAnalysisRequest

# from af.pipeline.data_reader import DataReaderFactory, PhenotypeData
# from af.pipeline.data_reader.models import Trait  # noqa: E402; noqa: E402
# from af.pipeline.data_reader.models import Experiment, Occurrence
# from af.pipeline.data_reader.models.enums import DataSource, DataType
# from af.pipeline.db import services
# from af.pipeline.db.core import DBConfig
# from af.pipeline.db.models import Property
# from af.pipeline.exceptions import DpoException, InvalidAnalysisRequest
# from af.pipeline.pandasutil import df_keep_columns


class ProcessData(ABC):
    """Abstract class for ProcessData objects"""

    @abstractmethod
    def get_traits(self):
        pass

    @abstractmethod
    def seml(self):
        pass

    @abstractmethod
    def sesl(self):
        pass

    @abstractmethod
    def mesl(self):
        pass

    @abstractmethod
    def meml(self):
        pass

    @abstractmethod
    def run(self):
        pass


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

    ProcessData(analysis_request).run()
