#!/usr/bin/env python3

# to manage module imports when run in slurm or run directly from celery,
# when called, pipeline python script should append parent directory to sys path,
# so pipeline as a module can be imported by both celery task and slurm script.
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


from pipeline.data_reader import DataReaderFactory, PhenotypeData  # noqa: E402
from pipeline.data_reader.exceptions import (
    DataSourceNotAvailableError,
    DataTypeNotAvailableError,
    MissingTaskParameter)  # noqa: E402
from pipeline.data_reader.models import Experiment, Occurrence, Trait  # noqa: E402
from pipeline.data_reader.models.enums import DataSource, DataType  # noqa: E402

import pipeline.config  # noqa: E402

from pandas import DataFrame  # noqa: E402


class ProcessData:

    def __init__(
            self,
            data_source: str,
            api_base_url: str,
            api_token: str,
            analysis_request,
            analysis_config):
        """ Pre process input data before inputing into analytical engine.
        """
        try:
            self.data_source: DataSource = DataSource[data_source]
        except KeyError:
            raise DataSourceNotAvailableError(data_source)
        factory = DataReaderFactory(self.data_source)
        self.data_reader: PhenotypeData = factory.get_phenotype_data(
            api_base_url=api_base_url, api_bearer_token=api_token)
        self.analysis_request = analysis_request
        self.analysis_config = analysis_config

    def _get_plots(self, occurrence_ids: list[str]) -> DataFrame:
        plots = DataFrame()
        for occurrence_id in occurrence_ids:
            plots_by_occurrence_id = self.data_reader.get_plots(occurrence_id)
            plots = plots.append(plots_by_occurrence_id)
        return plots

    def _get_plot_measurements(self, occurrence_ids: list[str]) -> DataFrame:
        plot_measurements = DataFrame()
        for occurrence_id in occurrence_ids:
            plot_measurements_by_occurrence_id = self.data_reader.get_plot_measurements(occurrence_id)
            plot_measurements = plot_measurements.append(plot_measurements_by_occurrence_id)
        return plot_measurements

    def run(self):
        occurrence_ids = self.analysis_request["data"]["occurrence_id"]
        _plots = self._get_plots(occurrence_ids)
        _plot_measurements = self._get_plot_measurements(occurrence_ids)

        plots_and_measurements = _plots.merge(_plot_measurements, on="plot_id")

        print(plots_and_measurements)


if __name__ == '__main__':
    ProcessData("EBS", "http://api.google.com", "", "", "").run()
