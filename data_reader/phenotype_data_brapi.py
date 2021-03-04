import pandas as pd

from models.experiment import Experiment
from models.trait import Trait

from data_reader.phenotype_data import PhenotypeData


SEARCH_PLOTS_BY_OCCURRENCE_URL = ("/observationunits"
                                  "?observationUnitLevelName=plot")


class PhenotypeDataBrapi(PhenotypeData):
    """ reads phenotype data from a brapi ebs data source .
    """

    API_FIELDS_TO_LOCAL_FIELDS = {
    }

    def get_plots_by_occurrence_id(self,
                                   occurrence_id: int = None) -> pd.DataFrame:
        raise NotImplementedError

    def get_plots_measurements_by_occurrence_id(
            self,
            occurrence_id: int = None) -> pd.DataFrame:
        raise NotImplementedError

    def get_experiment(self, experiment_id: int = None) -> Experiment:
        raise NotImplementedError

    def get_trait(self, trait_id: int = None) -> Trait:
        raise NotImplementedError
