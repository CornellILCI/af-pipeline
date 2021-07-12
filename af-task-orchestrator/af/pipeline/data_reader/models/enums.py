from enum import Enum


class DataType(Enum):
    PHENOTYPE = 1
    GENOTYPE = 2


class DataSource(str, Enum):
    EBS = "EBS"
    BRAPI = "BRAPI"
