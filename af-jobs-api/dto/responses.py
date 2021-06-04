from datetime import datetime

from dto.enums import AnalysisTypeEnum
from pydantic import BaseModel
from typing import Optional


class AnalysisRequest(BaseModel):
    requestId: str
    crop: str
    institute: str
    analysisType: AnalysisTypeEnum
    status: str
    createdOn: datetime
    modifiedOn: Optional[datetime]
