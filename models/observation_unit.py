from pydantic import BaseModel


class ObservationUnitPathParams(BaseModel):
    observationUnitDbId: str = None
    studyDbId: str = None
    observationLevel: str = None
    pageSize: int = None
    page: int = None
