from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import MagicMock, patch

from af.pipeline.data_reader.models import Trait
from af.pipeline.db.models import Property
from af.pipeline.dpo import ProcessData
from pandas import DataFrame

from conftest import get_json_resource, get_test_analysis_request


def get_job_file_template():
    return (
        "{job_file_id}\n"
        "\tloc !A !SORTALL !PRUNEALL\n"
        "\texpt !A !LL 32\n"
        "\tentry !A \n"
        "\tplot !A \n"
        "\tcol !I \n"
        "\trow !I \n"
        "\trep !A \n"
        "{trait_abbreviation}\n"
        "{job_file_path}.csv !CSV !SKIP 1 !AKAIKE !NODISPLAY 1 "
        "!MVINCLUDE !MAXIT 250 !EXTRA 10 !TXTFORM 1 !FCON !SUM !OUTLIER\n"
        "tabulate {trait_abbreviation} ~ entry\n"
        "{trait_abbreviation} ~ mu rep !r entry !f mv\n"
        "residual ar1(row).ar1(col)\n"
        "prediction entry !PRESENT entry !SED !TDIFF\n"
    )


def get_exploc_analysis_pattern():
    return Property(code="SESL")


def get_analysis_fields():
    return [
        type(
            "PropertyResult",
            (object,),
            {
                "Property": Property(code="loc", data_type="!A"),
                "property_meta": {"definition": "loc_id", "condition": "!SORTALL !PRUNEALL"},
            },
        ),
        type(
            "PropertyResult",
            (object,),
            {
                "Property": Property(code="expt", data_type="!A"),
                "property_meta": {"definition": "expt_id", "condition": "!LL 32"},
            },
        ),
        type(
            "PropertyResult",
            (object,),
            {"Property": Property(code="entry", data_type="!A"), "property_meta": {"definition": "entry_id"}},
        ),
        type(
            "PropertyResult",
            (object,),
            {"Property": Property(code="plot", data_type="!A"), "property_meta": {"definition": "plot_id"}},
        ),
        type(
            "PropertyResult",
            (object,),
            {"Property": Property(code="col", data_type="!I"), "property_meta": {"definition": "pa_x"}},
        ),
        type(
            "PropertyResult",
            (object,),
            {"Property": Property(code="row", data_type="!I"), "property_meta": {"definition": "pa_y"}},
        ),
        type(
            "PropertyResult",
            (object,),
            {"Property": Property(code="rep", data_type="!A"), "property_meta": {"definition": "rep_factor"}},
        ),
    ]


def get_asreml_option():
    return [
        Property(
            statement="!CSV !SKIP 1 !AKAIKE !NODISPLAY 1 !MVINCLUDE !MAXIT 250 !EXTRA 10 !TXTFORM 1 !FCON !SUM !OUTLIER"
        )
    ]


def get_tabulate():
    return [Property(statement="{trait_name} ~ entry")]


def get_formula():
    return Property(statement="{trait_name} ~ mu rep !r entry !f mv")


def get_residual():
    return Property(statement="ar1(row).ar1(col)")


def get_prediction():
    return Property(statement="entry !PRESENT entry !SED !TDIFF")


class TestProcessData(TestCase):
    @patch("af.pipeline.config.get_asreml_input_directory")
    @patch("af.pipeline.db.services.get_analysis_config_properties")
    @patch("af.pipeline.db.services.get_analysis_config_module_fields")
    @patch("af.pipeline.db.services.get_property")
    @patch("af.pipeline.data_reader.DataReaderFactory.get_phenotype_data")
    def test_dpo_sesl_filter(
        self, mock_phenotype_ebs, mock_get_property,
        mock_get_analysis_fields, mock_get_analysis_config_properties, asreml_input_folder
    ):

        test_request = get_test_analysis_request()
        output_folder = TemporaryDirectory()
        asreml_input_folder.return_value = output_folder.name

        phenotype_data_ebs_instance = MagicMock()
        mock_plots = []
        plots_columns = [
            "plot_id",
            "expt_id",
            "loc_id",
            "occurr_id",
            "entry_id",
            "pa_x",
            "pa_y",
            "rep_factor",
            "blk",
            "plot_qc",
        ]

        # for occurrence id 1
        mock_plots.append(
            DataFrame(
                columns=plots_columns,
                data=[
                    [2909, 1, 1, 1, 1, 1, 1, 1, 1, "G"],
                    [2910, 1, 1, 1, 1, 1, 2, 1, 1, "G"],
                ],
            )
        )

        # for occurrence id 2
        mock_plots.append(
            DataFrame(
                columns=plots_columns,
                data=[
                    [2911, 1, 1, 2, 1, 2, 1, 1, 1, "G"],
                    [2912, 1, 1, 2, 1, 2, 2, 1, 1, "G"],
                ],
            )
        )

        phenotype_data_ebs_instance.get_plots.side_effect = mock_plots

        mock_plot_measurements = []
        plot_measurements_columns = ["plot_id", "trait_id", "trait_qc", "trait_value"]

        # for occurrence id 1 and trait id 1
        mock_plot_measurements.append(
            DataFrame(
                columns=plot_measurements_columns,
                data=[
                    [2909, 1, "G", 6.155850575],
                    [2910, 1, "G", 6.751358238],
                ],
            )
        )

        # for occurrence id 2 and trait id 1
        mock_plot_measurements.append(DataFrame(columns=plot_measurements_columns, data=[]))
        phenotype_data_ebs_instance.get_plot_measurements.side_effect = mock_plot_measurements

        mock_traits = []
        test_trait = {"trait_id": 1, "trait_name": "trait_name_1", "abbreviation": "trait_abbrev_1"}
        mock_traits.append(Trait(**test_trait))
        phenotype_data_ebs_instance.get_trait.side_effect = mock_traits

        mock_phenotype_ebs.return_value = phenotype_data_ebs_instance

        mock_get_property.side_effect = [get_exploc_analysis_pattern(), get_formula(), get_residual(), get_prediction()]
        mock_get_analysis_fields.return_value = get_analysis_fields()
        mock_get_analysis_config_properties.side_effect = [get_asreml_option(), get_tabulate()]

        expected_data_file_contents = (
            "loc,expt,entry,plot,col,row,rep,trait_abbrev_1\n"
            "1,1,1,2909,1,1,1,6.155850575\n"
            "1,1,1,2910,1,2,1,6.751358238\n"
            "1,1,1,2911,2,1,1,NA\n"
            "1,1,1,2912,2,2,1,NA\n"
        )

        expected_job_file_1 = get_job_file_template().format(
            job_file_id="test_id_1",
            job_file_path=f"{output_folder.name}/test_id_1",
            trait_abbreviation="trait_abbrev_1",
        )

        results = ProcessData(test_request).run()

        self.assertEqual(len(results), 1)

        self.assertTrue("asreml_job_file" in results[0])
        with open(results[0]["asreml_job_file"]) as job_f_:
            job_file_contents = job_f_.read()
            self.assertEqual(job_file_contents, expected_job_file_1)

        self.assertTrue("data_file" in results[0])
        with open(results[0]["data_file"]) as data_f_:
            data_file_contents = data_f_.read()
            self.assertEqual(data_file_contents, expected_data_file_contents)

    @patch("af.pipeline.config.get_asreml_input_directory")
    @patch("af.pipeline.db.services.get_analysis_config_properties")
    @patch("af.pipeline.db.services.get_analysis_config_module_fields")
    @patch("af.pipeline.db.services.get_property")
    @patch("af.pipeline.data_reader.DataReaderFactory.get_phenotype_data")
    def test_dpo_seml_filter(
        self, mock_phenotype_ebs, mock_get_property,
        mock_get_analysis_fields, mock_get_analysis_config_properties, asreml_input_folder
    ):

        test_request = get_test_analysis_request()
        output_folder = TemporaryDirectory()
        asreml_input_folder.return_value = output_folder.name

        phenotype_data_ebs_instance = MagicMock()

        mock_plots = []
        plots_columns = [
            "plot_id",
            "expt_id",
            "loc_id",
            "occurr_id",
            "entry_id",
            "pa_x",
            "pa_y",
            "rep_factor",
            "blk",
            "plot_qc",
        ]

        # for occurrence id 1
        mock_plots.append(
            DataFrame(
                columns=plots_columns,
                data=[
                    [2909, 1, 1, 1, 1, 1, 1, 1, 1, "G"],
                    [2910, 1, 1, 1, 1, 1, 2, 1, 1, "G"],
                ],
            )
        )

        # for occurrence id 2
        mock_plots.append(
            DataFrame(
                columns=plots_columns,
                data=[
                    [2911, 1, 1, 2, 1, 2, 1, 1, 1, "G"],
                    [2912, 1, 1, 2, 1, 2, 2, 1, 1, "G"],
                ],
            )
        )

        phenotype_data_ebs_instance.get_plots.side_effect = mock_plots

        mock_plot_measurements = []
        plot_measurements_columns = ["plot_id", "trait_id", "trait_qc", "trait_value"]

        # for occurrence id 1 and trait id 1
        mock_plot_measurements.append(
            DataFrame(
                columns=plot_measurements_columns,
                data=[
                    [2909, 1, "G", 6.155850575],
                    [2910, 1, "G", 6.751358238],
                ],
            )
        )

        # for occurrence id 2 and trait id 1
        mock_plot_measurements.append(DataFrame(columns=plot_measurements_columns, data=[]))
        phenotype_data_ebs_instance.get_plot_measurements.side_effect = mock_plot_measurements

        mock_traits = []
        test_trait = {"trait_id": 1, "trait_name": "trait_name_1", "abbreviation": "trait_abbrev_1"}
        mock_traits.append(Trait(**test_trait))
        phenotype_data_ebs_instance.get_trait.side_effect = mock_traits

        expected_data_file_1_contents = (
            "loc,expt,entry,plot,col,row,rep,trait_abbrev_1\n"
            "1,1,1,2909,1,1,1,6.155850575\n"
            "1,1,1,2910,1,2,1,6.751358238\n"
        )

        expected_data_file_2_contents = (
            "loc,expt,entry,plot,col,row,rep,trait_abbrev_1\n" "1,1,1,2911,2,1,1,NA\n" "1,1,1,2912,2,2,1,NA\n"
        )

        expected_job_file_1 = get_job_file_template().format(
            job_file_id="test_id_1",
            job_file_path="{output_folder.name}/test_id_1",
            trait_abbreviation="trait_abbrev_1",
        )

        expected_job_file_1 = get_job_file_template().format(
            job_file_id="test_id_1_1",
            job_file_path=f"{output_folder.name}/test_id_1_1",
            trait_abbreviation="trait_abbrev_1",
        )

        expected_job_file_2 = get_job_file_template().format(
            job_file_id="test_id_2_1",
            job_file_path=f"{output_folder.name}/test_id_2_1",
            trait_abbreviation="trait_abbrev_1",
        )

        mock_phenotype_ebs.return_value = phenotype_data_ebs_instance

        exploc_analysis_pattern = get_exploc_analysis_pattern()
        exploc_analysis_pattern.code = "SEML"
        mock_get_property.side_effect = [
            exploc_analysis_pattern,
            get_formula(),
            get_residual(),
            get_prediction(),
            get_formula(),
            get_residual(),
            get_prediction(),
        ]
        mock_get_analysis_fields.return_value = get_analysis_fields()
        mock_get_analysis_config_properties.side_effect = [
            get_asreml_option(),
            get_tabulate(),
            get_asreml_option(),
            get_tabulate(),
        ]
        results = ProcessData(test_request).run()

        self.assertEqual(len(results), 2)

        self.assertTrue("asreml_job_file" in results[0])
        with open(results[0]["asreml_job_file"]) as job_f_:
            job_file_contents = job_f_.read()
            self.assertEqual(job_file_contents, expected_job_file_1)

        self.assertTrue("data_file" in results[0])
        with open(results[0]["data_file"]) as data_f_:
            data_file_contents = data_f_.read()
            self.assertEqual(data_file_contents, expected_data_file_1_contents)

        self.assertTrue("asreml_job_file" in results[1])
        with open(results[1]["asreml_job_file"]) as job_f_:
            job_file_contents = job_f_.read()
            self.assertEqual(job_file_contents, expected_job_file_2)

        self.assertTrue("data_file" in results[1])
        with open(results[1]["data_file"]) as data_f_:
            data_file_contents = data_f_.read()
            self.assertEqual(data_file_contents, expected_data_file_2_contents)
