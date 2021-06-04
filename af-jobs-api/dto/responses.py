from datetime import datetime
from typing import Optional

from dto.enums import AnalysisTypeEnum
from pydantic import BaseModel


class AnalysisRequest(BaseModel):
    requestId: str
    crop: str
    institute: str
    analysisType: AnalysisTypeEnum
    status: str
    createdOn: datetime
    modifiedOn: Optional[datetime]
