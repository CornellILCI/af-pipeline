import pandas as pd

from models import Experiment, Occurrence, Trait

from data_reader.phenotype_data import PhenotypeData


SEARCH_PLOTS_BY_OCCURRENCE_URL = ("/observationunits"
                                  "?observationUnitLevelName=plot")


class PhenotypeDataBrapi(PhenotypeData):
    """ reads phenotype data from a brapi ebs data source .
    """

    API_FIELDS_TO_LOCAL_FIELDS = {
    }

    def get_plots(self, occurrence_id: int = None) -> pd.DataFrame:
        raise NotImplementedError

    def get_plot_measurements(
            self,
            occurrence_id: int = None) -> pd.DataFrame:
        raise NotImplementedError

    def get_occurrence(self, occurrence_id: int = None) -> Occurrence:
        raise NotImplementedError

    def get_experiment(self, experiment_id: int = None) -> Experiment:
        raise NotImplementedError

    def get_trait(self, trait_id: int = None) -> Trait:
        raise NotImplementedError
