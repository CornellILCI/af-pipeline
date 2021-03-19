from pydantic import BaseModel


class ObservationQueryParams(BaseModel):
    observationDbId: str = None
    studyDbId: str = None
    observationLevel: str = None
    pageSize: int = None
    page: int = None
