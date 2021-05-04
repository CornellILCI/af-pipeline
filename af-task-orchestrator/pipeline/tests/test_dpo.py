
from pipeline.data_reader import DataReaderFactory, PhenotypeData

from pipeline.dpo import ProcessData


class TestProcessData:

    @patch("pipeline.data_reader.phenotype.get_plots")
    @patch("pipeline.data_reader.phenotype.get_plot_measurements")
    def test_run_sesl_filter(self, mock_get_plots, mock_get_plot_measurements):
        pass
