from abc import ABC, abstractmethod
import pandas as pd

from models.experiment import Experiment
from models.trait import Trait


class PhenotypeData(ABC):
    """ Abstract class for reading phenotype data from different kinds of
    data sources
    """

    @abstractmethod
    def get_plots_by_occurence_id(self, occurrence_id: str) -> pd.Dataframe:
        pass

    @abstractmethod
    def get_plots_measurement_by_occurrce_id(self,
                                             occurrence_id: str
                                             ) -> pd.Dataframe:
        pass

    @abstractmethod
    def get_experiment(self, experiment_id: str) -> Experiment:
        pass

    @abstractmethod
    def get_trait(self, trait_id: str) -> Trait:
        pass
