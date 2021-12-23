from common.api_models import (
    Property,
    ErrorResponse,
    Metadata,
    PaginationQueryParameters,
    create_metadata,
    map_property
)
from pydantic import BaseModel, Field
from typing import List, Optional

class AnalysisConfigsFilterParamerters(BaseModel):
    engine: Optional[str] = Field(None, description="Name of the analysis engine")
    design: Optional[str] = Field(None, description="Design type")
    traitLevel: Optional[str] = Field(None, description="Trait level, example: plot")
    analysisObjective: Optional[str] = Field(None, description="Analysis objective example: prediction")
    experimentAnalysisPattern: Optional[str] = Field(None, description="Experiment Analysis pattern example: single")
    locationAnalysisPattern: Optional[str] = Field(None, description="Location Analysis pattern example: single")
    traitPattern: Optional[str] = Field(None, description="Trait Pattern example: single")

class AnalysisConfigsListQueryParameters(PaginationQueryParameters, AnalysisConfigsFilterParamerters):
    pass

class AnalysisConfigListResponseResult(BaseModel):
    data: Optional[List[Property]] = None


class AnalysisConfigListResponse(BaseModel):
    metadata: Optional[Metadata] = None
    result: Optional[AnalysisConfigListResponseResult] = None

