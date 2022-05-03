from typing import List, Optional
from datetime import datetime

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


class AfBaseModel(BaseModel):
    createdOn: Optional[datetime] = None
    modifiedOn: Optional[datetime] = None


class AnalysisConfigCreateObject(BaseModel):
    code: str = Field(None, description="Organization code")
    configName: str = Field(None, description="config name")
    label: str = Field(None, description="label")
    description: str = Field(None, description="Description")
    design: str = Field(None, description="Design type")
    dataType: str = Field(None, description="data type")
    creatorId: str = Field(None, description="creator id")
    modifierId: str = Field(None, description="modifier id")
    tenantId: str = Field(None, description="tenant id")
    statement: str = Field(None, description="statement")
    propertyMetaVersion: str = Field(None, description="Version")
    propertyMetaDate: str = Field(None, description="Date")
    propertyMetaAuthor: str = Field(None, description="Author")
    propertyMetaEmail: str = Field(None, description="Email")
    propertyMetaOrganizationCode: str = Field(None, description="Organization code")
    propertyMetaEngine: str = Field(None, description="engine")
    propertyMetaBreedingProgramId: str = Field(None, description="Breeding ProgramId")
    propertyMetaPipelineId: str = Field(None, description="Pipeline Id")
    propertyMetaStageId: str = Field(None, description="Stage Id")
    propertyMetaDesign: str = Field(None, description="Design")
    propertyMetaTraitLevel: str = Field(None, description="Trait Level")
    propertyMetaAnalysisObjective: str = Field(None, description="Analysis Objective")
    propertyMetaExpAnalysisPattern: str = Field(None, description="Experiment Analysis Pattern")
    propertyMetaLocAnalysisPattern: str = Field(None, description="Location Analysis Pattern")
    propertyMetaYearAnalysisPattern: str = Field(None, description="Yearly Analysis Pattern")
    propertyMetaTraitPattern: str = Field(None, description="Trait Pattern")


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