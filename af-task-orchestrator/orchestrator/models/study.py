from datetime import datetime

from pydantic import BaseModel


class Study(BaseModel):
    active: bool = None
    endDate: str = None
    growthFacility: str = None
    contacts: str = None
    locationName: str = None
    seasons: list = None
    environmentParameters: list = None
    externalReferences: str = None
    dataLinks: list = None
    studyDescription: str = None
    commonCropName: str = None
    studyType: str = None
    lastUpdate: datetime = None
    additionalInfo: dict = {}
    studyCode: str = None
    studyDbId: str
    studyPUI: str = None
    culturalPractices: str = None
    observationUnitsDescription: str = None
    studyName: str = None
    observationLevels: str = None
    trialName: str = None
    documentationURL: str = None
    trialDbId: str
    experimentalDesign: str = None
    license: str = None
    startDate: datetime = None
    locationDbId: str
