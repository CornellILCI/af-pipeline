# generated by datamodel-codegen:
#   filename:  apiv1.yaml
#   timestamp: 2021-06-23T20:14:46+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    pageSize: int = Field(
        ...,
        description=(
            "The number of data elements returned, aka the size of the current page."
            "If the requested page does not have enough elements to fill a page at the requested page size, "
            "this field should indicate the actual number of elements returned."
        ),
        example=1000,
    )
    currentPage: int = Field(
        ...,
        description=(
            "The index number for the returned page of data. "
            "This should always match the requested page number or the default page (0)."
        ),
        example=0,
    )


class PaginationQueryParameters(BaseModel):
    pageSize: int = Field(1000, description=("The size of the pages to be returned. Default is 1000."), ge=0)
    page: int = Field(0, description=("Used to request a specific page of data to be returned"), ge=0)


class ErrorResponse(BaseModel):
    errorMsg: Optional[str] = Field(None, description="Reason or cause of errors.")


class AnalysisType(str, Enum):
    ANALYZE = "ANALYZE"
    RANDOMIZE = "RANDOMIZE"


class Status(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN-PROGRESS"
    DONE = "DONE"
    FAILURE = "FAILURE"


class DataSource(str, Enum):
    EBS = "EBS"
    BRAPI = "BRAPI"


class Property(BaseModel):
    propertyId: Optional[str] = Field(None, description="Id of the property")
    propertyName: Optional[str] = Field(None, description="Name of the property")
    propertyCode: Optional[str] = Field(None, description="Property code.")
    label: Optional[str] = Field(None, description="Label for user view.")
    type: Optional[str] = Field(
        None, description="Classifier of properties within its context (e.g. catalog_item, catalog_root)"
    )
    createdOn: Optional[datetime] = None
    modifiedOn: Optional[datetime] = None
    createdBy: Optional[str] = Field(None, description="Id of the user who created the property.")
    modifiedBy: Optional[str] = Field(None, description="Id of the user who modified the property.")
    isActive: Optional[bool] = Field(True, description="Whether the property is active in the system.")
    statement: Optional[str] = Field(
        None, description="A command, instruction, piece of code, etc., associated to the property"
    )


class PropertyListResponseResult(BaseModel):
    data: Optional[List[Property]] = None

class Metadata(BaseModel):
    pagination: Optional[Pagination] = None


class PropertyListResponse(BaseModel):
    metadata: Optional[Metadata] = None
    result: Optional[PropertyListResponseResult] = None

def create_metadata(current_page, page_size):
    return Metadata(
        pagination=Pagination(
            currentPage=current_page,
            pageSize=page_size
        )
    )

