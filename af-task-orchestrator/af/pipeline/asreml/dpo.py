import os
import pathlib
from collections import OrderedDict

from af.pipeline import config
from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.data_reader import DataReaderFactory, PhenotypeData
from af.pipeline.data_reader.models import Trait  # noqa: E402; noqa: E402

# from af.pipeline.data_reader.models import Experiment, Occurrence
# from af.pipeline.data_reader.models.enums import DataSource, DataType
from af.pipeline.db import services
from af.pipeline.db.core import DBConfig
from af.pipeline.dpo import ProcessData

# from af.pipeline.db.models import Property
from af.pipeline.exceptions import DpoException
from af.pipeline.pandasutil import df_keep_columns


class AsremlProcessData(ProcessData):
    def __init__(self, analysis_request: AnalysisRequest):
        """Constructor.

        Args:
            analysis_request: Object with all required inputs to run analysis.
        """

        self.analysis_request = analysis_request

        factory = DataReaderFactory(analysis_request.dataSource.name)
        self.data_reader: PhenotypeData = factory.get_phenotype_data(
            api_base_url=analysis_request.dataSourceUrl, api_bearer_token=analysis_request.dataSourceAccessToken
        )

        self.occurrence_ids = analysis_request.occurrenceIds
        self.trait_ids = analysis_request.traitIds
        self.db_session = DBConfig.get_session()

        self.analysis_fields = None
        self.input_fields_to_config_fields = None

        self.output_folder = analysis_request.outputFolder

    def get_traits(self) -> list[Trait]:
        traits = []
        for trait_id in self.trait_ids:
            trait: Trait = self.data_reader.get_trait(trait_id)
            traits.append(trait)
        return traits

    def seml(self):
        """For Single Experiment Single Location

        Generator for ASReml job definition file and input data files for each trait.

        Raises:
            DpoException when invalid request paramters is passed.
            DataReaderException when unable to extract data from datasource.
        """

        plots_by_occurrence_id = {}

        traits: list[Trait] = self.get_traits()

        for occurrence_id in self.occurrence_ids:
            plots_by_occurrence_id[occurrence_id] = self.data_reader.get_plots(occurrence_id)

        for trait in traits:

            plots_and_measurements = None

            for occurrence_id in self.occurrence_ids:

                plots = plots_by_occurrence_id[occurrence_id]
                plot_measurements_ = self.data_reader.get_plot_measurements(occurrence_id, trait.trait_id)

                _plots_and_measurements = plots.merge(plot_measurements_, on="plot_id", how="left")
                if plots_and_measurements is None:
                    plots_and_measurements = _plots_and_measurements
                else:
                    plots_and_measurements = plots_and_measurements.append(_plots_and_measurements)

            plots_and_measurements = self._format_result_data(plots_and_measurements, trait)

            if not plots_and_measurements.empty:
                job_input_files = self._write_job_input_files(f"{trait.trait_id}", plots_and_measurements, trait)
                yield job_input_files

    def sesl(self):
        """For Single Experiment Multi Location

        Generator for ASReml job definition file and input data files for each valid combination of trait
        and occurrence.

        Raises:
            DpoException when invalid request paramters is passed.
            DataReaderException when unable to extract data from datasource.
        """

        traits: list[Trait] = self.get_traits()

        for occurrence_id in self.occurrence_ids:
            plots = self.data_reader.get_plots(occurrence_id)
            for trait in traits:
                plot_measurements_ = self.data_reader.get_plot_measurements(occurrence_id, trait.trait_id)

                # default is inner join
                plots_and_measurements = plots.merge(plot_measurements_, on="plot_id", how="left")

                plots_and_measurements = self._format_result_data(plots_and_measurements, trait)

                if not plots_and_measurements.empty:
                    job_input_files = self._write_job_input_files(
                        f"{occurrence_id}_{trait.trait_id}", plots_and_measurements, trait
                    )
                    yield job_input_files

    def _format_result_data(self, plots_and_measurements, trait):

        input_fields_to_config_fields = self._get_input_fields_config_fields()

        # drop trait id
        plots_and_measurements.drop(["trait_id"], axis=1, inplace=True)

        # fill trait value with NA string
        plots_and_measurements[["trait_value"]] = plots_and_measurements[["trait_value"]].fillna(
            config.UNIVERSAL_UNKNOWN
        )

        # map trait value column to trait name
        input_fields_to_config_fields["trait_value"] = trait.abbreviation

        # Key only the config field columns
        plots_and_measurements = df_keep_columns(plots_and_measurements, input_fields_to_config_fields.keys())

        plots_and_measurements = plots_and_measurements.rename(columns=input_fields_to_config_fields)

        plots_and_measurements = plots_and_measurements[input_fields_to_config_fields.values()]

        return plots_and_measurements

    def _write_job_input_files(self, job_id, job_data, trait):

        # request_id = self.analysis_request.requestId

        job_name = f"{self.analysis_request.requestId}_{job_id}"

        job_file_name = f"{job_name}.as"
        data_file_name = f"{job_name}.csv"

        job_file_path = os.path.join(self.output_folder, job_name, job_file_name)
        data_file_path = os.path.join(self.output_folder, job_name, data_file_name)

        # create parent directories
        os.makedirs(pathlib.Path(job_file_path).parent)

        job_data.to_csv(data_file_path, index=False)

        job_file_lines = self._get_asrml_job_file_lines(job_name, data_file_path, trait)

        with open(job_file_path, "w") as j_f:
            for line in job_file_lines:
                j_f.write("{}\n".format(line))

        return {"data_file": data_file_path, "asreml_job_file": job_file_path, "job_name": job_name}

    def _get_analysis_fields(self):
        if not self.analysis_fields:
            self.analysis_fields = services.get_analysis_config_module_fields(
                self.db_session, self.analysis_request.analysisConfigPropertyId
            )
        return self.analysis_fields

    def _get_input_fields_config_fields(self):
        """Map of input data fields to analysis configuration fields."""
        if not self.input_fields_to_config_fields:

            self.input_fields_to_config_fields = OrderedDict()

            analysis_fields = self._get_analysis_fields()

            for field in analysis_fields:
                input_field_name = field.property_meta.get("definition")

                if input_field_name is None:
                    raise DpoException("Analysis config fields have no definition")

                self.input_fields_to_config_fields[input_field_name] = field.Property.code
        return self.input_fields_to_config_fields

    def _get_asrml_job_file_lines(self, job_name, data_file_path, trait: Trait):

        analysis_config_id = self.analysis_request.analysisConfigPropertyId

        # 1: add command line options that has to go before everything
        job_file_lines = ["!XML"]

        # 2: add title of the analysis run
        job_file_lines.append(job_name)

        # 3: adding the analysis field statements
        for field_line in self._get_analysis_field_lines(analysis_config_id):
            job_file_lines.append(field_line)

        # 4: adding trait name
        job_file_lines.append(trait.abbreviation)

        # 5: adding otpions
        asreml_option = self._get_asreml_option(analysis_config_id)
        options_line = "{} {}".format(data_file_path, asreml_option.statement)
        job_file_lines.append(options_line)

        # 6: adding tabulate
        tabulate = self._get_tabulate(analysis_config_id)
        tabulate_line = "tabulate {}".format(tabulate.statement.format(trait_name=trait.abbreviation))
        job_file_lines.append(tabulate_line)

        # 7: adding formula
        formula = services.get_property(self.db_session, self.analysis_request.configFormulaPropertyId)
        formula_statement = formula.statement.format(trait_name=trait.abbreviation)
        job_file_lines.append(formula_statement)

        # 8: adding residual
        residual = services.get_property(self.db_session, self.analysis_request.configResidualPropertyId)
        # residual_statement = residual.statement
        job_file_lines.append(f"residual {residual.statement}")

        # 9: adding prediction
        prediction = services.get_property(self.db_session, "19")
        prediction_statement = "prediction {}".format(prediction.statement)
        job_file_lines.append(prediction_statement)

        return job_file_lines

    def _get_asreml_option(self, analysis_config_id: str):
        asreml_options = services.get_analysis_config_properties(self.db_session, analysis_config_id, "asrmel_options")
        if len(asreml_options) > 0:
            return asreml_options[0]
        else:
            raise DpoException("No ASREML engine options found.")

    def _get_tabulate(self, analysis_config_id: str):
        tabulate = services.get_analysis_config_properties(self.db_session, analysis_config_id, "tabulate")
        if len(tabulate) > 0:
            return tabulate[0]
        else:
            raise DpoException("No analysis config tabulate found.")

    def _get_analysis_field_lines(self, analysis_config_id: str):
        analysis_fields = services.get_analysis_config_module_fields(self.db_session, analysis_config_id)
        if len(analysis_fields) == 0:
            raise DpoException("No Analysis fields found.")
        for field in analysis_fields:
            field_line = "\t{stat_factor} {data_type} {condition}".format(
                stat_factor=field.Property.code,
                data_type=field.Property.data_type,
                condition=field.property_meta.get("condition", ""),
            )
            yield field_line

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
        else:
            raise DpoException(f"Analysis pattern value: {exptloc_analysis_pattern} is invalid")

        for job_input in job_inputs_gen:
            job_inputs.append(job_input)

        return job_inputs