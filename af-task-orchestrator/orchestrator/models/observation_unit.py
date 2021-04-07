from pydantic import BaseModel


class ObservationUnitQueryParams(BaseModel):
    observationUnitDbId: str = None
    studyDbId: str = None
    observationLevel: str = None
    pageSize: int = None
    page: int = None
