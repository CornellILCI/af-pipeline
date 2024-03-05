from enum import Enum


class DataSourceEnum(str, Enum):
    EBS = "EBS"
    BRAPI = "BRAPI"


class AnalysisTypeEnum(str, Enum):
    ANALYZE = "ANALYZE"
    RANDOMIZE = "RANDOMIZE"
