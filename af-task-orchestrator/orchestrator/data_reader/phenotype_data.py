from abc import ABC, abstractmethod

import pandas as pd
from data_reader.data_reader import DataReader
from models import Experiment, Occurrence, Trait


class PhenotypeData(ABC, DataReader):
    """Interface for reading phenotype data from different kinds of
    data sources
    """

    @abstractmethod
    def get_plots(self, occurrence_id: str) -> pd.DataFrame:
        """Gets plots as pandas dataframe.

        Args:
            occurrence_id: To get plots belonging to the given occurrence id.

        Returns:
            Plot data as pandas dataframe.
        """
        pass

    @abstractmethod
    def get_plot_measurements(self, occurrence_id: str) -> pd.DataFrame:
        """Gets plot measurements as pandas dataframe.

        Args:
            occurrence_id: To get plot measurements belonging
            to the given occurrence id.

        Returns:
            Plot data as pandas dataframe.

        Raises:
            DataReaderException when failed to fetch data.
        """
        pass

    @abstractmethod
    def get_occurrence(seld, occurrence_id: str) -> Occurrence:
        """Gets Occurrence for given occurrence id.

        Plots belongs to occurrence.

        Args:
            occurrence_id: Id of the occurrence.

        Returns:
            Requested Occurrence object.

        Raises:
            DataReaderException when failed to fetch data.
        """
        pass

    @abstractmethod
    def get_experiment(self, experiment_id: str) -> Experiment:
        """Gets Experiment for given experiment id.

        Occurrences belong to Experiment.

        Args:
            experiment_id: Id of the experiment.

        Returns:
            Requested Experiment object.

        Raises:
            DataReaderException when failed to fetch data.
        """
        pass

    @abstractmethod
    def get_trait(self, trait_id: str) -> Trait:
        """Gets Trait for given trait id.

        Variable for which plot measurement are made. eg., plant height.

        Args:
            trait_id: Id of the trait.

        Returns:
            Requested Trait object.
        """
        pass
