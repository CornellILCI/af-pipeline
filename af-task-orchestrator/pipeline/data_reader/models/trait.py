from pydantic import BaseModel


class Trait(BaseModel):
    trait_id: int
    trait_name: str
    abbrevation: str


class VariableEbs(BaseModel):
    variableDbId: int
    abbrev: str
    label: str = None
    name: str
    dataType: str = None
    notNull: bool = None
    type: str = None
    status: str = None
    displayName: str = None
    ontologyReference: str = None
    bibliographicalReference: str = None
    targetTable: str = None
    targetModel: str = None
    propertyDbId: int = None
    property: str = None
    methodDbId: int = None
    methodName: str = None
    methodDescription: str = None
    scaleDbId: int = None
    scaleName: str = None
    scaleType: str = None
    variableSet: str = None
    synonym: str = None
    remarks: str = None
    creationTimestamp: str = None
    creatorDbId: int = None
    creator: str = None
    modificationTimestamp: str = None
    modifierDbId: int = None
    modifier: str = None
    description: str = None
    defaultValue: str = None
    usage: str = None
    dataLevel: str = None
    isComputed: bool = None
