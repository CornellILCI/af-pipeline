# flake8: noqa
# TODO: discus N815 flake8 warning
from datetime import datetime

from pydantic import BaseModel


class Occurrence(BaseModel):
    occurrence_id: int
    occurrence_name: str
    experiment_id: int
    experiment_name: str
    location_id: int
    location: str
    rep_count: int = None
    entry_count: int = None
    plot_count: int = None


class OccurrenceEbs(BaseModel):
    occurrenceDbId: int
    occurrenceName: str
    experimentDbId: int
    experiment: str
    locationDbId: int
    location: str
    repCount: int = None
    entryCount: int = None
    plotCount: int = None
    occurrenceCode: str = None
    occurrenceNumber: int = None
    programDbId: int = None
    programCode: str = None
    program: str = None
    projectDbId: int = None
    projectCode: str = None
    project: str = None
    siteDbId: int = None
    siteCode: str = None
    site: str = None
    fieldDbId: int = None
    fieldCode: str = None
    field: str = None
    geospatialObjectId: int = None
    geospatialObjectCode: str = None
    geospatialObject: str = None
    geospatialObjectType: str = None
    experimentDbId: int = None
    experimentCode: str = None
    experiment: str = None
    experimentType: str = None
    experimentStatus: str = None
    experimentStageDbId: str = None
    experimentStageCode: str = None
    experimentStage: str = None
    experimentYear: int = None
    experimentSeasonDbId: int = None
    experimentSeasonCode: str = None
    experimentSeason: str = None
    experimentDesignType: str = None
    experimentStewardDbId: int = None
    experimentSteward: str = None
    dataProcessDbId: int = None
    dataProcessAbbrev: str = None
    occurrenceStatus: str = None
    description: str = None
    contactPerson: str = None
    creationTimestamp: str = None
    creatorDbId: str = None
    creator: str = None
    modificationTimestamp: datetime = None
    modifierDbId: str = None
    modifier: str = None
    occurrenceDocument: str = None
