from pipeline.data_reader.models.enums import DataSource
from pydantic import BaseModel, conlist


class AnalysisRequest(BaseModel):
    requestId: str
    dataSource: DataSource
    dataSourceUrl: str
    dataSourceAccessToken: str
    experimentIds: conlist(str, min_items=1)
    occurrenceIds: conlist(str, min_items=1)
    traitIds: conlist(str, min_items=1)
    analysisObjectivePropertyId: str
    analysisConfigPropertyId: str
    expLocAnalysisPatternPropertyId: str
    configFormulaPropertyId: str
    configResidualPropertyId: str
    outputFolder: str
