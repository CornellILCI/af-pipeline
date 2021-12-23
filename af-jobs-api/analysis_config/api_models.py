from typing import List, Optional

from common.api_models import (
    ErrorResponse,
    Metadata,
    PaginationQueryParameters,
    Property,
    create_metadata,
    map_property,
)
from pydantic import BaseModel, Field


class AnalysisConfigsFilterParamerters(BaseModel):
    engine: Optional[str] = Field(None, description="Name of the analysis engine")
    design: Optional[str] = Field(None, description="Design type")
    traitLevel: Optional[str] = Field(None, description="Trait level, example: plot")
    analysisObjective: Optional[str] = Field(None, description="Analysis objective example: prediction")
    experimentAnalysisPattern: Optional[str] = Field(None, description="Experiment Analysis pattern example: single")
    locationAnalysisPattern: Optional[str] = Field(None, description="Location Analysis pattern example: single")
    traitPattern: Optional[str] = Field(None, description="Trait Pattern example: single")

    def as_db_filter_params(self):
        return {
            "engine": self.engine,
            "design": self.design,
            "trait_level": self.traitLevel,
            "analysis_objective": self.analysisObjective,
            "exp_analysis_pattern": self.experimentAnalysisPattern,
            "loc_analysis_pattern": self.locationAnalysisPattern,
            "trait_pattern": self.traitPattern,
        }


class AnalysisConfigsListQueryParameters(PaginationQueryParameters, AnalysisConfigsFilterParamerters):
    pass


class AnalysisConfigListResponseResult(BaseModel):
    data: Optional[List[Property]] = None


class AnalysisConfigListResponse(BaseModel):
    metadata: Optional[Metadata] = None
    result: Optional[AnalysisConfigListResponseResult] = None
