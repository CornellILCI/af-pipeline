from typing import List, Optional

from dto.enums import AnalysisTypeEnum, DataSourceEnum
from pydantic import BaseModel


class AnalysisRequestParameters(BaseModel):
    dataSource: DataSourceEnum
    dataSourceUrl: str
    dataSourceAccessToken: str
    crop: Optional[str]
    institute: Optional[str]
    analysisType: Optional[AnalysisTypeEnum] = AnalysisTypeEnum.ANALYZE
    experimentIds: List[str]
    occurrenceIds: List[str]
    traitIds: List[str]
    analysisObjectivePropertyId: str
    analysisConfigPropertyId: str
    expLocAnalysisPatternPropertyId: str
    configFormulaPropertyId: str
    configResidualPropertyId: str
