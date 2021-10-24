from datetime import datetime
from enum import Enum
from typing import List, Optional

from common.api_models import (
    AnalysisType,
    DataSource,
    ErrorResponse,
    Metadata,
    PaginationQueryParameters,
    Status,
    create_metadata,
)
from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    requestId: Optional[str] = None
    requestorId: Optional[str] = None
    crop: Optional[str] = Field(None, description="Name of the crop")
    institute: Optional[str] = Field(None, description="Name of the institute for which the analysis is submitted.")
    analysisType: Optional[AnalysisType] = None
    status: Optional[Status] = None
    createdOn: Optional[datetime] = None
    modifiedOn: Optional[datetime] = None
    resultDownloadRelativeUrl: Optional[str] = None
    configFormulaProperty = None


class AnalysisRequestParameters(BaseModel):
    dataSource: DataSource
    dataSourceUrl: str = Field(..., description="Base API url of datasource instance.")
    dataSourceAccessToken: str = Field(..., description="Bearer token to access datasource.")
    crop: Optional[str] = Field(None, description="Name of the crop")
    requestorId: Optional[str] = Field(None, description="Id of the user who submits analysis request.")
    institute: Optional[str] = Field(None, description="Name of the institute for which the analysis is submitted.")
    analysisType: Optional[AnalysisType] = AnalysisType.ANALYZE
    experimentIds: List[str]
    occurrenceIds: List[str]
    traitIds: List[str]
    analysisObjectivePropertyId: str = Field(..., description="Property Id of selected analysis objective.")
    analysisConfigPropertyId: str = Field(..., description="Property Id of selected analysis configuration.")
    expLocAnalysisPatternPropertyId: str = Field(
        ..., description="Property Id of selected experiment location analysis pattern."
    )
    configFormulaPropertyId: str = Field(..., description="Property Id of the formula to run the analysis.")
    configResidualPropertyId: str = Field(..., description="Property Id of the residual for the analysis model.")
    configPredictionPropertyIds: list[str] = Field([], description="Property Ids of predictions in the model.")


class AnalysisRequestListQueryParameters(PaginationQueryParameters):
    crop: Optional[str] = Field(None, description="Name of the crop")
    requestorId: Optional[str] = Field(None, description="Id of the user who submits analysis request.")
    institute: Optional[str] = Field(None, description="Name of the institute for which the analysis is submitted.")
    status: Optional[Status] = None


class AnalysisRequestResponse(BaseModel):
    result: AnalysisRequest = None


class AnalysisRequestListResponseResult(BaseModel):
    data: Optional[List[AnalysisRequest]] = None


class AnalysisRequestListResponse(BaseModel):
    metadata: Optional[Metadata] = None
    result: Optional[AnalysisRequestListResponseResult] = None
