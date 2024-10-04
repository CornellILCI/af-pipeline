from abc import ABC, abstractmethod
from typing import List

import pandas as pd
from af.pipeline.data_reader.data_reader import DataReader
from af.pipeline.data_reader.models import Experiment, Occurrence, Trait

from af.pipeline.data_reader.models.brapi.genotyping import Sample
from pandas import DataFrame

class PhenotypeData(ABC, DataReader):
    """Interface for reading phenotype data from different kinds of
    data sources
    """

    @abstractmethod
    def get_plots(self, experiment_id=None, occurrence_id: str = None, location_id=None) -> pd.DataFrame:
        """Gets plots as pandas dataframe.

        Args:
            occurrence_id: To get plots belonging to the given occurrence id.

        Returns:
            Plot data as pandas dataframe.
        """
        pass

    @abstractmethod
    def get_plot_measurements(self, occurrence_id: str, trait_id: str) -> pd.DataFrame:
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
    def get_occurrence(self, occurrence_id: str) -> Occurrence:
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
    
    @abstractmethod
    def get_samples(self, sample_ids: "list[str]"=None, observation_ids: "list[str]"=None, studyDbIds:"list[str]" = None) -> "list[Sample]":
        """Gets Sample for an identifier
        Primarily used to get a sample object related to an observation

        Args:
            sample_id (str, optional): sample id to search on if passed. Defaults to None.
            observation_id (str, optional): observation id to search on if passed. Defaults to None.

        Returns:
            Sample: Sample object
        """

    def get_samples_df(self, sample_ids: List[str]=None, observation_ids: List[str]=None,studyDbIds:List[str] = None, germplasmDbIds:List[str]=None) -> DataFrame:
        #Creating an object with 600+ columns to get two columns out - if you're wondering where the speedup can happen, it's here -JDLS
        #Also note, only implemented on the brapi side, so this is going to burn on the BMS side if not implemented 'correctly' -JDLS
        samples:List[Sample] = self.get_samples(sample_ids=sample_ids,observation_ids=observation_ids,studyDbIds=studyDbIds, germplasmDbIds=germplasmDbIds)#I hate everything about this.... study links exactly 2 things, ObservationUnit is linked to nothing. BYEARGh
        print(f"Sample example: {samples[:1]}")
        df_input=[{'observationUnitDbId':x.observationUnitDbId,'sampleDbId':x.sampleDbId, 'germplasmDbId':x.germplasmDbId} for x in samples]
        df = DataFrame(data=df_input,columns=['observationUnitDbId','sampleDbId', 'germplasmDbId'])
        #df = DataFrame(data)#, columns=cols)# In theory, columns should keep their names? So I don't _have_ to add a list of column names like the prototype I'm following - JDLS
        print(f"Sample dataframe default columns: {df.columns}")
        return df 