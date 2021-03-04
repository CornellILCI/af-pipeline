from abc import ABC, abstractmethod
import pandas as pd

from models.experiment import Experiment
from models.trait import Trait

from data_reader.data_reader import DataReader


class PhenotypeData(ABC, DataReader):
    """ Abstract class for reading phenotype data from different kinds of
    data sources
    """

    @abstractmethod
    def get_plots_by_occurrence_id(self, occurrence_id: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_plots_measurements_by_occurrence_id(self,
                                                occurrence_id: str
                                                ) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_experiment(self, experiment_id: str) -> Experiment:
        pass

    @abstractmethod
    def get_trait(self, trait_id: str) -> Trait:
        pass
