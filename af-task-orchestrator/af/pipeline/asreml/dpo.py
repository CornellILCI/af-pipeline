import os
import pathlib

import pandas as pd
from af.pipeline import config, pandasutil
from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.data_reader import DataReaderFactory, PhenotypeData
from af.pipeline.data_reader.models import Occurrence, Trait  # noqa: E402; noqa: E402
from af.pipeline.db import services
from af.pipeline.db.core import DBConfig
from af.pipeline.dpo import ProcessData
from af.pipeline.exceptions import DpoException
from af.pipeline.job_data import JobData
from af.pipeline.pandasutil import df_keep_columns


class AsremlProcessData(ProcessData):
    def __init__(self, analysis_request: AnalysisRequest):
        super().__init__(analysis_request)

    def __get_traits(self) -> list[Trait]:
        traits = []
        for trait_id in self.trait_ids:
            trait: Trait = self.data_reader.get_trait(trait_id)
            traits.append(trait)
        return traits

    def _save_metadata(self, job_name, metadata):

        metadata_file_path = self.get_meta_data_file_path(job_name)

        to_csv_kwargs = {"sep": "\t", "index": False}

        if os.path.isfile(metadata_file_path):
            to_csv_kwargs.update({"header": False, "mode": "a"})

        metadata.to_csv(metadata_file_path, **to_csv_kwargs)

        return metadata_file_path

    def _generate_metadata(self, plots, occurrence, trait):

        metadata_columns = ["entry_id", "entry_name", "entry_type"]
        metadata = plots.loc[:, metadata_columns]  # get a copy, not a view

        metadata["experiment_id"] = occurrence.experiment_id
        metadata["experiment_name"] = occurrence.experiment_name
        metadata["location_name"] = occurrence.location
        metadata["location_id"] = occurrence.location_id
        metadata["trait_abbreviation"] = trait.abbreviation

        return metadata

    def seml(self):
        """For Single Experiment Single Location

        Generator for ASReml job definition file and input data files for each trait.

        Raises:
            DpoException when invalid request paramters is passed.
            DataReaderException when unable to extract data from datasource.
        """

        plots_by_id = {}
        occurrences_by_id = {}

        traits: list[Trait] = self.__get_traits()

        num_occurrences = len(self.occurrence_ids)

        # read once
        for occurrence_id in self.occurrence_ids:
            plots_by_id[occurrence_id]: pd.DataFrame = self.data_reader.get_plots(occurrence_id=occurrence_id)
            occurrences_by_id[occurrence_id]: Occurrence = self.data_reader.get_occurrence(occurrence_id)

        for trait in traits:

            plots_and_measurements = None

            # processed input files and other metadata required to run the analysis
            job_data = JobData()

            job_name = f"{self.analysis_request.requestId}_{trait.trait_id}"
            job_data.job_name = job_name

            # -- BA-875 --
            job_data.trait_name = trait.abbreviation
            job_data.location_name = "Multi Location"

            for occurrence_id in self.occurrence_ids:

                plots = plots_by_id[occurrence_id]
                occurrence = occurrences_by_id[occurrence_id]
                job_data.occurrences.append(occurrence)

                if num_occurrences == 1:
                    job_data.location_name = occurrence.location

                # save metadata in plots
                metadata = self._generate_metadata(plots, occurrence, trait)
                job_data.metadata_file = self._save_metadata(job_name, metadata)

                plot_measurements_ = self.data_reader.get_plot_measurements(occurrence_id, trait.trait_id)

                _plots_and_measurements = plots.merge(plot_measurements_, on="plot_id", how="left")

                if plots_and_measurements is None:
                    plots_and_measurements = _plots_and_measurements
                else:
                    plots_and_measurements = plots_and_measurements.append(_plots_and_measurements)

            plots_and_measurements = self.format_input_data(plots_and_measurements, trait)

            if not plots_and_measurements.empty:
                self._write_job_data(job_data, plots_and_measurements, trait)
                yield job_data

    def sesl(self):
        """For Single Experiment Multi Location

        Generator for ASReml job definition file and input data files for each valid combination of trait
        and occurrence.

        Raises:
            DpoException when invalid request paramters is passed.
            DataReaderException when unable to extract data from datasource.
        """

        traits: list[Trait] = self.__get_traits()

        for occurrence_id in self.occurrence_ids:

            plots = self.data_reader.get_plots(occurrence_id=occurrence_id)
            occurrence: Occurrence = self.data_reader.get_occurrence(occurrence_id)

            for trait in traits:

                job_name = f"{self.analysis_request.requestId}_{occurrence_id}_{trait.trait_id}"

                # processed input files and other metadata required to run the analysis
                job_data = JobData()

                job_data.job_name = job_name
                job_data.occurrences.append(occurrence)

                # -- BA-875
                job_data.trait_name = trait.abbreviation
                job_data.location_name = occurrence.location

                # save metadata in plots
                metadata = self._generate_metadata(plots, occurrence, trait)
                job_data.metadata_file = self._save_metadata(job_name, metadata)

                plot_measurements_ = self.data_reader.get_plot_measurements(occurrence_id, trait.trait_id)

                # default is inner join
                plots_and_measurements = plots.merge(plot_measurements_, on="plot_id", how="left")

                plots_and_measurements = self.format_input_data(plots_and_measurements, trait)

                if not plots_and_measurements.empty:
                    self._write_job_data(job_data, plots_and_measurements, trait)
                    yield job_data

    def mesl(self):
        raise NotImplementedError("MESL analysis pattern is not implemented")

    def meml(self):
        raise NotImplementedError("MEML analysis pattern is not implemented")

    def _write_job_data(self, job_data, plots_and_measurements, trait):
        job_data.trait_name = trait.abbreviation

        data_file_name = f"{job_data.job_name}.csv"

        job_data.job_result_dir = self.get_job_folder(job_data.job_name)

        job_data.data_file = os.path.join(job_data.job_result_dir, data_file_name)

        # by default sort by columns 'row' and 'col'. row and col here denotes plot's row and column
        plots_and_measurements.row = pd.to_numeric(plots_and_measurements.row, errors="coerce")
        plots_and_measurements.col = pd.to_numeric(plots_and_measurements.col, errors="coerce")
        plots_and_measurements = plots_and_measurements.sort_values(by=["row", "col"])

        plots_and_measurements.to_csv(job_data.data_file, index=False)

        self._set_job_params(job_data, trait)

        return job_data

    def _set_job_params(self, job_data, trait):

        job_file_name = f"{job_data.job_name}.as"

        job_data.job_file = os.path.join(job_data.job_result_dir, job_file_name)

        job_file_lines = self._get_asreml_job_file_lines(job_data, trait)

        with open(job_data.job_file, "w") as j_f:
            for line in job_file_lines:
                j_f.write("{}\n".format(line))

    def _get_asreml_job_file_lines(self, job_data, trait: Trait):

        analysis_config_id = self.analysis_request.analysisConfigPropertyId

        # 1: add command line options that has to go before everything
        job_file_lines = ["!XML"]

        # 2: add title of the analysis run
        job_file_lines.append(job_data.job_name)

        # 3: adding the analysis field statements
        for field_line in self._get_analysis_field_lines():
            job_file_lines.append(field_line)

        # 4: adding trait name
        job_file_lines.append(trait.abbreviation)

        # 5: adding options
        asreml_option = self._get_asreml_option()
        options_line = f"{job_data.data_file} {asreml_option.statement}"
        job_file_lines.append(options_line)

        # 6: adding tabulate
        tabulate = self._get_tabulate()
        tabulate_line = "tabulate {}".format(tabulate.statement.format(trait_name=trait.abbreviation))
        job_file_lines.append(tabulate_line)

        # 7: adding formula
        job_file_lines.append(self._get_formula(trait))

        # 8: adding residual
        residual = self._get_residual()
        job_file_lines.append(f"residual {residual}")

        # 9: adding all the predictions if prediction not defined by the user.
        predictions = self._get_predictions()
        for prediction in predictions:
            job_file_lines.append(f"prediction {prediction.statement}")

        return job_file_lines

    def _get_asreml_option(self):
        asreml_options = services.get_analysis_config_properties(
            self.db_session, self.analysis_request.analysisConfigPropertyId, "asreml_options"
        )
        if len(asreml_options) > 0:
            return asreml_options[0]
        else:
            raise DpoException("No ASREML engine options found.")

    def _get_formula(self, trait):
        formula = services.get_property(self.db_session, self.analysis_request.configFormulaPropertyId)
        formula_statement = formula.statement.format(trait_name=trait.abbreviation)
        return formula_statement

    def _get_residual(self):
        residual = services.get_property(self.db_session, self.analysis_request.configResidualPropertyId)
        return residual.statement

    def _get_tabulate(self):
        tabulate = services.get_analysis_config_properties(
            self.db_session, self.analysis_request.analysisConfigPropertyId, "tabulate"
        )
        if len(tabulate) > 0:
            return tabulate[0]
        else:
            raise DpoException("No analysis config tabulate found.")

    def _get_analysis_field_lines(self):
        analysis_fields = services.get_analysis_config_module_fields(
            self.db_session, self.analysis_request.analysisConfigPropertyId
        )
        if len(analysis_fields) == 0:
            raise DpoException("No Analysis fields found.")
        for field in analysis_fields:
            field_line = "\t{stat_factor} {data_type} {condition}".format(
                stat_factor=field.Property.code,
                data_type=field.Property.data_type,
                condition=field.property_meta.get("condition", ""),
            )
            yield field_line

    def _get_predictions(self):

        predictions = []

        if len(self.analysis_request.configPredictionPropertyIds) == 0:
            predictions = services.get_analysis_config_properties(
                self.db_session, self.analysis_request.analysisConfigPropertyId, "prediction"
            )
        else:
            for prediction_property_id in self.analysis_request.configPredictionPropertyIds:
                predictions.append(services.get_property(self.db_session, prediction_property_id))

        return predictions
