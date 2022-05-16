from typing import Optional

from af.pipeline.data_reader.models.enums import DataSource
from pydantic import BaseModel, conlist


class Occurrence(BaseModel):
    occurrenceId: str
    occurrenceName: str
    locationId: Optional[str]
    locationName: Optional[str]


class Experiment(BaseModel):
    experimentId: str
    experimentName: str
    occurrences: Optional[list[Occurrence]]


class Trait(BaseModel):
    traitId: str
    traitName: str


class AnalysisRequest(BaseModel):
    requestId: str
    dataSource: DataSource
    dataSourceUrl: str
    dataSourceAccessToken: str
    experiments: list[Experiment]
    traits: list[Trait]
    analysisObjectivePropertyId: str
    analysisConfigPropertyId: str
    expLocAnalysisPatternPropertyId: str
    configFormulaPropertyId: str
    configResidualPropertyId: str
    configPredictionPropertyIds: list[str] = []
    outputFolder: str
    crop:Optional[str]
