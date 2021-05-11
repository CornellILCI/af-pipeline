from enum import Enum


class DataType(Enum):
    PHENOTYPE = 1
    GENOTYPE = 2


class DataSource(Enum):
    EBS = 1
    BRAPI = 2
