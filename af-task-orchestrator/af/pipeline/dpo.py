#!/usr/bin/env python3

import argparse
import json
import os

# import pathlib
import sys
from abc import ABC, abstractmethod

from collections import OrderedDict

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
from af.pipeline.data_reader.models import Trait  # noqa: E402; noqa: E402
from af.pipeline import config, pandasutil, utils
from af.pipeline.job_data import JobData, JobParams

# from af.pipeline.data_reader.models import Experiment, Occurrence
# from af.pipeline.data_reader.models.enums import DataSource, DataType
from af.pipeline.db import services
from af.pipeline.db.core import DBConfig
from af.pipeline.exceptions import DpoException, InvalidAnalysisRequest

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
        self.location_ids = []

        # extract ids from the experiment, occurrence and location ids from analysis request.
        _location_ids = set()
        for experiment in analysis_request.experiments:
            self.experiment_ids.append(experiment.experimentId)
            if experiment.occurrences is not None:
                for occurrence in experiment.occurrences:
                    self.occurrence_ids.append(occurrence.occurrenceId)
                    _location_ids.add(occurrence.locationId)
        self.location_ids = sorted(_location_ids)

        self.trait_ids = []
        self.trait_by_id = {}
        for trait in analysis_request.traits:
            self.trait_ids.append(trait.traitId)

        self.db_session = DBConfig.get_session()

        self.__analysis_fields = None
        self.input_fields_to_config_fields = None

        self.output_folder = analysis_request.outputFolder

    def get_job_folder(self, job_name: str) -> str:

        job_folder = os.path.join(self.output_folder, job_name)

        if not os.path.isdir(job_folder):
            # create parent directories
            os.makedirs(pathlib.Path(job_folder))

        return job_folder

    def get_meta_data_file_path(self, job_name: str) -> str:

        job_folder = self.get_job_folder(job_name)

        return os.path.join(job_folder, "metadata.tsv")

    def get_trait_by_id(self, trait_id: str) -> Trait:

        if trait_id not in self.trait_by_id:
            self.trait_by_id[trait_id] = self.data_reader.get_trait(trait_id)

        return self.trait_by_id[trait_id]

    def get_model_formula(self, trait) -> str:
        formula = services.get_property(self.db_session, self.analysis_request.configFormulaPropertyId)
        formula_statement = formula.statement.format(trait_name=trait.abbreviation)
        return formula_statement

    def get_model_residual(self) -> str:
        residual = services.get_property(self.db_session, self.analysis_request.configResidualPropertyId)
        return residual.statement

    def get_model_predictions(self) -> list[str]:

        predictions = []

        if len(self.analysis_request.configPredictionPropertyIds) == 0:
            predictions = services.get_analysis_config_properties(
                self.db_session, self.analysis_request.analysisConfigPropertyId, "prediction"
            )
        else:
            for prediction_property_id in self.analysis_request.configPredictionPropertyIds:
                predictions.append(services.get_property(self.db_session, prediction_property_id))

        return predictions

    @property
    def analysis_fields(self):
        if not self.__analysis_fields:
            self.__analysis_fields = services.get_analysis_config_module_fields(
                self.db_session, self.analysis_request.analysisConfigPropertyId
            )
        return self.__analysis_fields

    def __get_input_fields_config_fields(self):
        """Map of input data fields to analysis configuration fields."""
        if not self.input_fields_to_config_fields:

            self.input_fields_to_config_fields = OrderedDict()

            for field in self.analysis_fields:
                input_field_name = field.property_meta.get("definition")

                if input_field_name is None:
                    raise DpoException("Analysis config fields have no definition")

                self.input_fields_to_config_fields[input_field_name] = field.Property.code
        return self.input_fields_to_config_fields

    def _set_job_params(self, job_data, trait):

        formula = utils.parse_formula(self.get_model_formula(trait))

        job_params = JobParams(**formula, residual=self.get_model_residual(), predictions=[])

        # set predictions statements
        predictions = self.get_model_predictions()

        if not predictions:
            raise ValueError("Predictions are not available for the job to process")

        job_params.predictions = [prediction.statement for prediction in predictions]

        job_data.job_params = job_params

    def format_input_data(self, plots_and_measurements, trait):
        """
        Formats input data downloaded to analysis ready data.
        Makes sure the column names of the input data are mapped according to analysis config.
        """

        input_fields_to_config_fields = self.__get_input_fields_config_fields()

        # drop trait id
        plots_and_measurements.drop(["trait_id"], axis=1, inplace=True)

        # fill trait value with NA string
        plots_and_measurements[["trait_value"]] = plots_and_measurements[["trait_value"]].fillna(
            config.UNIVERSAL_UNKNOWN
        )

        trait_qc = plots_and_measurements.trait_qc

        # rename
        plots_and_measurements.loc[trait_qc == "B", "trait_value"] = "NA"

        # map trait value column to trait name
        input_fields_to_config_fields["trait_value"] = trait.abbreviation

        # Key only the config field columns
        plots_and_measurements = pandasutil.df_keep_columns(
            plots_and_measurements, input_fields_to_config_fields.keys()
        )

        plots_and_measurements = plots_and_measurements.rename(columns=input_fields_to_config_fields)

        plots_and_measurements = plots_and_measurements[input_fields_to_config_fields.values()]

        return plots_and_measurements

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
            List of JobData
            example:
                [
                    JobData(
                        job_name: str = "",
                        job_result_dir: str = "",
                        data_file: str = "",
                        job_file: str = "",
                        job_params: JobParams = JobParams(
                            formula: str = None,
                            residual: str = None,
                            predictions: list[str] = None,
                        )
                        metadata_file: str = "",
                        occurrences: list[Occurrence] = field(default_factory=list),
                        trait_name: str = "",
                        location_name: str = ""
                    )
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
        elif exptloc_analysis_pattern.code == "MEML":
            job_inputs_gen = self.meml()
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
