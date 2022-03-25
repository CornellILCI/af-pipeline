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

import pathlib

# from af.pipeline import config
from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.data_reader import DataReaderFactory, PhenotypeData
from af.pipeline.db.core import DBConfig
from af.pipeline.exceptions import InvalidAnalysisRequest

# from af.pipeline.data_reader.models import Trait  # noqa: E402; noqa: E402
# from af.pipeline.data_reader.models import Experiment, Occurrence
# from af.pipeline.data_reader.models.enums import DataSource, DataType
from af.pipeline.db import services
# from af.pipeline.db.models import Property
# from af.pipeline.exceptions import DpoException, InvalidAnalysisRequest
# from af.pipeline.pandasutil import df_keep_columns


class ProcessData(ABC):
    """Abstract class for ProcessData objects"""

    def __init__(self, analysis_request, *args, **kwargs):
        """Constructor.

        Args:
            analysis_request: Object with all required inputs to run analysis.
        """

        self.analysis_request = analysis_request

        factory = DataReaderFactory(analysis_request.dataSource.name)
        self.data_reader: PhenotypeData = factory.get_phenotype_data(
            api_base_url=analysis_request.dataSourceUrl, api_bearer_token=analysis_request.dataSourceAccessToken
        )

        self.experiment_ids = []
        self.occurrence_ids = []

        self.location_ids = set()

        for experiment in analysis_request.experiments:
            self.experiment_ids.append(experiment.experimentId)
            if experiment.occurrences is not None:
                for occurrence in experiment.occurrences:
                    self.occurrence_ids.append(occurrence.occurrenceId)
                    self.location_ids.add(occurrence.locationId)

        self.trait_ids = []
        for trait in analysis_request.traits:
            self.trait_ids.append(trait.traitId)

        self.db_session = DBConfig.get_session()

        self.analysis_fields = None
        self.input_fields_to_config_fields = None

        self.output_folder = analysis_request.outputFolder

    def get_job_folder(self, job_name: str) -> str:

        job_folder = os.path.join(self.output_folder, job_name)

        if not os.path.isdir(job_folder):
            # create parent directories
            os.makedirs(pathlib.Path(job_folder))

        return job_folder

    @abstractmethod
    def sesl(self):
        pass

    @abstractmethod
    def seml(self):
        pass

    @abstractmethod
    def mesl(self):
        pass

    @abstractmethod
    def mesl(self):
        pass

    def run(self):
        """Pre process input data before inputing into analytical engine.

        Extracts plots and plot measurements from api source.
        Prepares the extracted data to feed into analytical engine.

        Returns:
            List of object with following args,
                job_name: Name of the job
                data_file: File with input data
                asrml_job_file: File with job configuration specific to input request
            example:
                [
                    {
                        "job_name": "job1"
                        "data_file": "/test/test.csv",
                        "asreml_job_file": "/test/test.as"
                    }
                ]

        Raises:
            DpoException, DataReaderException
        """
        
        exptloc_analysis_pattern = services.get_property(
            self.db_session, self.analysis_request.expLocAnalysisPatternPropertyId
        )

        job_inputs = []

        if exptloc_analysis_pattern.code == "SESL":
            job_inputs_gen = self.sesl()
        elif exptloc_analysis_pattern.code == "SEML":
            job_inputs_gen = self.seml()
        elif exptloc_analysis_pattern.code == "MESL":
            job_inputs_gen = self.mesl()
        else:
            raise DpoException(f"Analysis pattern value: {exptloc_analysis_pattern} is invalid")

        for job_input in job_inputs_gen:
            job_inputs.append(job_input)

        return job_inputs


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
