import pandas as pd


class PhenotypeDataProcess:
    """Extract and Pre process input data.

    Extract Plots and Plot measurements data from Datasources of types
    EBS or BRAPI and pre processed before being inputed to analyze.
    """

    def __init__(self, pipeline_request=None):
        """
        """
        self.pipeline_request = pipeline_request
        self.request_parameters = pipeline_request["parameters"]
        self.request_config = request_parameters["config_file"]


    def _get_plots(self) -> pd.Dataframe:
        pass

    def _get_plot_measurements(self) -> pd.Dataframe:
        pass

    def run(self):

        #Get plots and plot measurements as Dataframes
        plots = self._get_plots()
        plot_measurements = self._get_plot_measurements()


