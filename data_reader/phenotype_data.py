from abc import ABC, abstractmethod
import pandas as pd

from models import Experiment, Trait, Occurrence

from data_reader.data_reader import DataReader


class PhenotypeData(ABC, DataReader):
    """ Abstract class for reading phenotype data from different kinds of
    data sources
    """

    @abstractmethod
    def get_plots(self, occurrence_id: str) -> pd.DataFrame:
        """Reads plots from api source and returns a dataframe."""
        pass

    @abstractmethod
    def get_plot_measurements(self, occurrence_id: str) -> pd.DataFrame:
        """Reads plot measurements from api source and returns a dataframe"""
        pass

    @abstractmethod
    def get_occurrence(seld, occurrence_id: str) -> Occurrence:
        """Returns occurrence for given id"""
        pass

    @abstractmethod
    def get_experiment(self, experiment_id: str) -> Experiment:
        """Returns an experiment for given id"""
        pass

    @abstractmethod
    def get_trait(self, trait_id: str) -> Trait:
        """Returns a trait for given trait id"""
        pass
