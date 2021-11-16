from abc import ABC, abstractmethod

import pandas as pd
from af.pipeline.data_reader.data_reader import DataReader
from af.pipeline.data_reader.models import Experiment, Occurrence, Trait


class GenotypeData(ABC, DataReader):
    """Interface for reading phenotype data from different kinds of
    data sources
    """
