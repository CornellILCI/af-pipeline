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

        test_request["data"]["occurrence_id"] = [1, 2]
        test_request["data"]["trait_id"] = [1]

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

        mock_get_plots.side_effect = mock_plots

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
        mock_get_plot_measurements.side_effect = mock_plot_measurements

        mock_traits = []
        test_trait = {"trait_id": 1, "trait_name": "trait_name_1", "abbreviation": "trait_abbrev_1"}
        mock_traits.append(Trait(**test_trait))
        mock_get_trait.side_effect = mock_traits

        expected_columns = ""
        for field in test_config["Analysis_Module"]["fields"]:
            expected_columns += field["stat_factor"] + ","
        expected_columns += "trait_abbrev_1"

        expected_data_file_contents = (
            "loc,expt,entry,plot,col,row,rep,trait_abbrev_1\n"
            "1,1,1,2909,1,1,1,6.155850575\n"
            "1,1,1,2910,1,2,1,6.751358238\n"
            "1,1,1,2911,2,1,1,NA\n"
            "1,1,1,2912,2,2,1,NA\n"
        )

        expected_job_file_1 = get_job_file_template().format(
            job_file_id="test_id_1",
            trait_abbreviation="trait_abbrev_1",
        )

        output_folder = TemporaryDirectory()

        results = ProcessData("EBS", "http://test.org", "test").run(test_request, test_config, output_folder.name)

        self.assertEqual(len(results), 1)

        self.assertTrue("asreml_job_file" in results[0])
        with open(results[0]["asreml_job_file"]) as job_f_:
            job_file_contents = job_f_.read()
            self.assertEqual(job_file_contents, expected_job_file_1)

        self.assertTrue("data_file" in results[0])
        with open(results[0]["data_file"]) as data_f_:
            data_file_contents = data_f_.read()
            print(data_file_contents)
            print(expected_data_file_contents)
            self.assertEqual(data_file_contents, expected_data_file_contents)

    @patch("pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_trait")
    @patch("pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plot_measurements")
    @patch("pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plots")
    def test_dpo_seml_filter(self, mock_get_plots, mock_get_plot_measurements, mock_get_trait):
        pass
