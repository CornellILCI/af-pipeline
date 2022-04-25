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


class Analysis(AfBaseModel):
    code: str = Field(None, description="Organization code")
    configName: str = Field(None, description="config name")
    label: str = Field(None, description="label")
    description: str = Field(None, description="Description")
    design: str = Field(None, description="Design type")
    dataType: str = Field(None, description="data type")
    creatorId: str = Field(None, description="creator id")
    modifierId: str = Field(None, description="modifier id")
    isVoid: str = Field(None, description="is void")
    tenantId: str = Field(None, description="tenant id")
    id: str = Field(None, description="id")
    statement: str = Field(None, description="statement")


class AnalysisConfigMeta(AfBaseModel):
    propertyId : str = Field(None, description="property id")
    code: str = Field(None, description="Organization code")
    value: str = Field(None, description="value")
    tenantId: str = Field(None, description="tenant id")


class AnalysisConfig(AfBaseModel):
    order: str = Field(None, description="Order number")
    creatorId: str = Field(None, description="creator id")
    isVoid: str = Field(None, description="is void")
    propertyId: str = Field(None, description="property id")
    configPropertyId: str = Field(None, description="property id")
    isLayout: str = Field(None, description="property id")

    # configId: str = Field(None, description="config id")
    # configVersion: str = Field(None, description="config version")
    # createdOn: datetime = None
    # author: str = Field(None, description="author")
    # email: str = Field(None, description="email")
    # engine: str = Field(None, description="Name of the analysis engine")
    # experimentInfo: str = Field(None, description="experiment info")
    # breedingProgramId: str = Field(None, description="breeding program id")
    # pipelineId: str = Field(None, description="Description")
    # stageId: str = Field(None, description="stage id")
    # design: str = Field(None, description="Design type")
    # traitLevel: str = Field(None, description="Trait level, example: plot")
    # analysisInfo: str = Field(None, description="analysis info")
    # analysisObjective: str = Field(None, description="Analysis objective example: prediction")
    # experimentAnalysisPattern: str = Field(None, description="Experiment Analysis pattern example: single")
    # locationAnalysisPattern: str = Field(None, description="Location Analysis pattern example: single")
    # yearAnalysisPattern: str = Field(None, description="Description")
    # traitPattern: str = Field(None, description="Trait Pattern example: single")
    # # are some of these supposed to be Property objects instead of strings?
