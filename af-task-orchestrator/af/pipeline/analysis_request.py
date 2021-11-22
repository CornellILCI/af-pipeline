from af.pipeline.data_reader.models.enums import DataSource
from pydantic import BaseModel, conlist


class Experiment(BaseModel):
    experimentId: str
    experimentName: str


class Occurrence(BaseModel):
    occurrenceId: str
    occurrenceName: str


class Trait(BaseModel):
    traitId: str
    traitName: str


class AnalysisRequest(BaseModel):
    requestId: str
    dataSource: DataSource
    dataSourceUrl: str
    dataSourceAccessToken: str
    experiments: list[Experiment]
    occurrences: list[Occurrence]
    traits: list[Trait]
    analysisObjectivePropertyId: str
    analysisConfigPropertyId: str
    expLocAnalysisPatternPropertyId: str
    configFormulaPropertyId: str
    configResidualPropertyId: str
    configPredictionPropertyIds: list[str] = []
    outputFolder: str
