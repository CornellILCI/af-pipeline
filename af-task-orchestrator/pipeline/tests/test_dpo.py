from pipeline.data_reader import DataReaderFactory, PhenotypeData
from pipeline.dpo import ProcessData
from unittest import TestCase
from unittest.mock import Mock, patch

from tempfile import TemporaryDirectory

from conftest import get_json_resource

from pipeline.data_reader.models import Trait

import pandas as pd
from pandas import DataFrame

from pandas._testing import assert_frame_equal


mock_occurrence_ids = [1, 2, 3]
mock_trait_ids = [1, 2]


def get_mock_plots():
    mock_plots = []
    plots_columns = [
        "plot_id", "expt_id", "loc_id", "occurr_id", "entry_id", "pa_x", "pa_y",
        "rep_factor", "blk", "plot_qc"
    ]

    # for occurrence id 1
    mock_plots.append(DataFrame(
        columns=plots_columns,
        data=[
            [2909, 1, 1, 1, 1, 1, 1, 1, 1, "G"],
            [2910, 1, 1, 1, 1, 1, 2, 1, 1, "G"],
        ]
    ))

    # for occurrence id 2
    mock_plots.append(DataFrame(
        columns=plots_columns,
        data=[
            [2911, 1, 1, 2, 1, 2, 1, 1, 1, "G"],
            [2912, 1, 1, 2, 1, 2, 2, 1, 1, "G"],
        ]
    ))

    # for occurrence id 3
    mock_plots.append(DataFrame(
        columns=plots_columns,
        data=[
            [2913, 1, 1, 3, 1, 3, 1, 1, 1, "G"],
            [2914, 1, 1, 3, 1, 3, 2, 1, 1, "G"],
        ]
    ))
    return mock_plots


def get_mock_plot_measurements():

    mock_plot_measurements = []
    plot_measurements_columns = ["plot_id", "trait_id", "trait_qc", "trait_value"]

    # for trait 1
    mock_plot_measurements.append(DataFrame(
        columns=plot_measurements_columns,
        data=[
            [2909, 1, "G", 6.155850575],
            [2910, 1, "G", 6.751358238],
        ]
    ))
    mock_plot_measurements.append(DataFrame(
        columns=plot_measurements_columns,
        data=[
            [2911, 1, "G", 6.155850575],
            [2912, 1, "G", 6.751358238],
        ]
    ))
    mock_plot_measurements.append(DataFrame(
        columns=plot_measurements_columns,
        data=[]
    ))

    # for trait 2
    mock_plot_measurements.append(DataFrame(
        columns=plot_measurements_columns,
        data=[
            [2909, 2, "G", 6.155850575],
            [2910, 2, "G", 6.751358238],
        ]
    ))

    mock_plot_measurements.append(DataFrame(
        columns=plot_measurements_columns,
        data=[]
    ))
    mock_plot_measurements.append(DataFrame(
        columns=plot_measurements_columns,
        data=[]
    ))

    return mock_plot_measurements


def get_mock_plot_measurements_seml():

    mock_plot_measurements = []
    plot_measurements_columns = ["plot_id", "trait_id", "trait_qc", "trait_value"]

    mock_plot_measurements.append(DataFrame(
        columns=plot_measurements_columns,
        data=[
            [2909, 1, "G", 6.155850575],
            [2910, 1, "G", 6.751358238],
        ]
    ))
    mock_plot_measurements.append(DataFrame(
        columns=plot_measurements_columns,
        data=[
            [2909, 2, "G", 6.155850575],
            [2910, 2, "G", 6.751358238],
        ]
    ))

    mock_plot_measurements.append(DataFrame(
        columns=plot_measurements_columns,
        data=[
            [2911, 1, "G", 6.155850575],
            [2912, 1, "G", 6.751358238],
        ]
    ))
    mock_plot_measurements.append(DataFrame(
        columns=plot_measurements_columns,
        data=[]
    ))

    mock_plot_measurements.append(DataFrame(
        columns=plot_measurements_columns,
        data=[]
    ))
    mock_plot_measurements.append(DataFrame(
        columns=plot_measurements_columns,
        data=[]
    ))

    return mock_plot_measurements


def get_mock_traits():

    mock_traits = []

    test_trait = {
        "trait_id": 1,
        "trait_name": "trait_name_1",
        "abbreviation": "trait_abbrev_1"
    }
    mock_traits.append(Trait(**test_trait))

    test_trait = {
        "trait_id": 2,
        "trait_name": "trait_name_2",
        "abbreviation": "trait_abbrev_2"
    }
    mock_traits.append(Trait(**test_trait))
    return mock_traits


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
        "{job_file_id}.csv !CSV !SKIP 1 !AKAIKE !NODISPLAY 1 "
        "!MVINCLUDE !MAXIT 250 !EXTRA 10 !TXTFORM 1 !FCON !SUM !OUTLIER\n"
        "tabulate {trait_abbreviation} ~ entry\n"
        "{trait_abbreviation} ~ mu rep !r entry !f mv\n"
        "residual ar1(row).ar1(col)\n"
        "prediction entry !PRESENT entry !SED !TDIFF\n"
    )


class TestProcessData(TestCase):

    @patch("pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_trait")
    @patch("pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plot_measurements")
    @patch("pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plots")
    def test_dpo_sesl_filter(self, mock_get_plots, mock_get_plot_measurements, mock_get_trait):

        test_request = get_json_resource(__file__, "test_analysis_request.req")
        test_config = get_json_resource(__file__, "test_analysis_config.cfg")

        test_request["metadata"]["id"] = "test_id"

        # set analysis pattern to 1 so sesl filter will be called.
        test_request["parameters"]["exptloc_analysis_pattern"] = 1

        test_request["data"]["occurrence_id"] = mock_occurrence_ids
        test_request["data"]["trait_id"] = mock_trait_ids

        mock_get_plots.side_effect = get_mock_plots()
        mock_get_plot_measurements.side_effect = get_mock_plot_measurements()
        mock_get_trait.side_effect = get_mock_traits()

        expected_file_1_data = DataFrame(
            columns=["plot", "trait_abbrev_1", "row", "col", "rep", "entry", "expt", "loc"],
            data=[
                [2909, 6.155850575, 1, 1, 1, 1, 1, 1],
                [2910, 6.751358238, 2, 1, 1, 1, 1, 1],
                [2911, 6.155850575, 1, 2, 1, 1, 1, 1],
                [2912, 6.751358238, 2, 2, 1, 1, 1, 1],
                [2913, "NA", 1, 3, 1, 1, 1, 1],
                [2914, "NA", 2, 4, 1, 1, 1, 1],
            ]
        )

        expected_file_2_data = DataFrame(
            columns=["plot", "trait_abbrev_2", "row", "col", "rep", "entry", "expt", "loc"],
            data=[
                [2909, 6.155850575, 1, 1, 1, 1, 1, 1],
                [2910, 6.751358238, 2, 1, 1, 1, 1, 1],
                [2911, "NA", 1, 2, 1, 1, 1, 1],
                [2912, "NA", 2, 2, 1, 1, 1, 1],
                [2913, "NA", 1, 3, 1, 1, 1, 1],
                [2914, "NA", 2, 4, 1, 1, 1, 1],
            ]
        )

        expected_job_file_1 = get_job_file_template().format(
            job_file_id="test_id_1", trait_abbreviation="trait_abbrev_1",
        )

        expected_job_file_1 = get_job_file_template().format(
            job_file_id="test_id_2", trait_abbreviation="trait_abbrev_2",
        )

        output_folder = TemporaryDirectory()

        results = ProcessData("EBS", "http://test.org", "test").run(test_request, test_config, output_folder.name)

        self.assertEqual(len(results), 2)

        self.assertTrue("asreml_job_file" in results[0])
        with open(results[0]["asreml_job_file"]) as job_f_:
            job_file_contents = job_f_.read()
            self.assertEqual(job_file_contents, expected_job_file_1)

        self.assertTrue("asreml_job_file" in results[1])
        with open(results[1]["asreml_job_file"]) as job_f_:
            job_file_contents = job_f_.read()
            self.assertEqual(job_file_contents, expected_job_file_2)

        self.assertTrue("data_file" in results[0])
        result_data_1 = pd.read_csv(results[0]["data_file"])
        result_data_1 = result_data_1[expected_file_1_data.columns]
        assert_frame_equal(result_data_1, expected_file_1_data)

        self.assertTrue("data_file" in results[1])
        result_data_2 = pd.read_csv(results[1]["data_file"])
        result_data_2 = result_data_2[expected_file_2_data.columns]
        assert_frame_equal(result_data_2, expected_file_2_data)

    @patch("pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_trait")
    @patch("pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plot_measurements")
    @patch("pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plots")
    def test_dpo_seml_filter(self, mock_get_plots, mock_get_plot_measurements, mock_get_trait):

        test_request = get_json_resource(__file__, "test_analysis_request.req")
        test_config = get_json_resource(__file__, "test_analysis_config.cfg")

        test_request["metadata"]["id"] = "test_id"

        # set analysis pattern to 1 so sesl filter will be called.
        test_request["parameters"]["exptloc_analysis_pattern"] = 2

        test_request["data"]["occurrence_id"] = mock_occurrence_ids
        test_request["data"]["trait_id"] = mock_trait_ids

        mock_get_plots.side_effect = get_mock_plots()
        mock_get_plot_measurements.side_effect = get_mock_plot_measurements_seml()
        mock_get_trait.side_effect = get_mock_traits()

        expected_file_1_data = DataFrame(
            columns=["plot", "trait_abbrev_1", "row", "col", "rep", "entry", "expt", "loc"],
            data=[
                [2909, 6.155850575, 1, 1, 1, 1, 1, 1],
                [2910, 6.751358238, 2, 1, 1, 1, 1, 1],
            ]
        )

        expected_file_2_data = DataFrame(
            columns=["plot", "trait_abbrev_2", "row", "col", "rep", "entry", "expt", "loc"],
            data=[
                [2909, 6.155850575, 1, 1, 1, 1, 1, 1],
                [2910, 6.751358238, 2, 1, 1, 1, 1, 1],
            ]
        )

        expected_file_3_data = DataFrame(
            columns=["plot", "trait_abbrev_1", "row", "col", "rep", "entry", "expt", "loc"],
            data=[
                [2911, 6.155850575, 1, 2, 1, 1, 1, 1],
                [2912, 6.751358238, 2, 2, 1, 1, 1, 1],
            ]
        )

        expected_file_4_data = DataFrame(
            columns=["plot", "trait_abbrev_2", "row", "col", "rep", "entry", "expt", "loc"],
            data=[
                [2911, "NA", 1, 2, 1, 1, 1, 1],
                [2912, "NA", 2, 2, 1, 1, 1, 1],
            ]
        )

        expected_file_5_data = DataFrame(
            columns=["plot", "trait_abbrev_1", "row", "col", "rep", "entry", "expt", "loc"],
            data=[
                [2911, "NA", 1, 2, 1, 1, 1, 1],
                [2912, "NA", 2, 2, 1, 1, 1, 1],
            ]
        )

        expected_file_5_data = DataFrame(
            columns=["plot", "trait_abbrev_1", "row", "col", "rep", "entry", "expt", "loc"],
            data=[
                [2911, "NA", 1, 2, 1, 1, 1, 1],
                [2912, "NA", 2, 2, 1, 1, 1, 1],
            ]
        )

        expected_job_file_1 = get_job_file_template().format(
            job_file_id="test_id_1_1", trait_abbreviation="trait_abbrev_1",
        )

        expected_job_file_2 = get_job_file_template().format(
            job_file_id="test_id_1_2", trait_abbreviation="trait_abbrev_2",
        )

        expected_job_file_3 = get_job_file_template().format(
            job_file_id="test_id_2_1", trait_abbreviation="trait_abbrev_1",
        )

        expected_job_file_4 = get_job_file_template().format(
            job_file_id="test_id_2_2", trait_abbreviation="trait_abbrev_2",
        )

        expected_job_file_5 = get_job_file_template().format(
            job_file_id="test_id_3_1", trait_abbreviation="trait_abbrev_1",
        )

        expected_job_file_6 = get_job_file_template().format(
            job_file_id="test_id_3_2", trait_abbreviation="trait_abbrev_2",
        )

        output_folder = TemporaryDirectory()

        results = ProcessData("EBS", "http://test.org", "test").run(test_request, test_config, output_folder.name)

        self.assertEqual(len(results), 6)

        self.assertTrue("asreml_job_file" in results[0])
        with open(results[0]["asreml_job_file"]) as job_f_:
            job_file_contents = job_f_.read()
            self.assertEqual(job_file_contents, expected_job_file_1)

        self.assertTrue("asreml_job_file" in results[1])
        with open(results[1]["asreml_job_file"]) as job_f_:
            job_file_contents = job_f_.read()
            self.assertEqual(job_file_contents, expected_job_file_2)

        self.assertTrue("asreml_job_file" in results[2])
        with open(results[2]["asreml_job_file"]) as job_f_:
            job_file_contents = job_f_.read()
            self.assertEqual(job_file_contents, expected_job_file_3)

        self.assertTrue("data_file" in results[0])
        result_data_1 = pd.read_csv(results[0]["data_file"])
        result_data_1 = result_data_1[expected_file_1_data.columns]
        assert_frame_equal(result_data_1, expected_file_1_data)

        self.assertTrue("data_file" in results[1])
        result_data_2 = pd.read_csv(results[1]["data_file"])
        result_data_2 = result_data_2[expected_file_2_data.columns]
        assert_frame_equal(result_data_2, expected_file_2_data)

        self.assertTrue("data_file" in results[2])
        result_data_3 = pd.read_csv(results[2]["data_file"])
        result_data_3 = result_data_3[expected_file_3_data.columns]
        assert_frame_equal(result_data_3, expected_file_3_data)
