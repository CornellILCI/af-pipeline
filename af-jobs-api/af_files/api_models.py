from datetime import datetime
from typing import Optional 
from pydantic import BaseModel


class JobFile(BaseModel):

    fileName: str = None
    fileDownloadRelativeUrl: str = None
    createdOn: Optional[datetime] = None
    modifiedOn: Optional[datetime] = None

