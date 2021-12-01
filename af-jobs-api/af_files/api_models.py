from datetime import datetime
from typing import Optional 
from pydantic import BaseModel


class File(BaseModel):

    fileName: str = None
    createdOn: Optional[datetime] = None
    modifiedOn: Optional[datetime] = None

