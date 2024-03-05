from typing import Optional

from af.pipeline.data_reader.models.enums import DataSource
from pydantic import BaseModel, conlist, Field


class Occurrence(BaseModel):
    occurrenceId: str
    occurrenceName: str
    locationId: Optional[str]
    locationName: Optional[str]


class Experiment(BaseModel):
    experimentId: str
    experimentName: str
    occurrences: Optional['list[Occurrence]']


class Trait(BaseModel):
    traitId: str
    traitName: str


class AnalysisRequest(BaseModel):
    requestId: str
    dataSource: DataSource
    dataSourceUrl: str 
    dataSourceAccessToken: str
    genoSource: Optional[DataSource] = Field(None)#TODO - genoSource is a terrible hack to get a separate genotype database entry.
    genoSourceUrl: Optional[str] = Field(None)
    genoSourceAccessToken: Optional[str]= Field(None)
    genoConnectionType: Optional[str] = Field(None)#How to get geno from pheno data, bit TODO
    genoConnectionAction: Optional[str] = Field(None) #How to combine geno/pheno data - 
    genoStudyIds:Optional['list[str]']=Field(None)
    experiments: 'list[Experiment]'
    traits: 'list[Trait]'
    analysisObjectivePropertyId: str
    analysisConfigPropertyId: str
    expLocAnalysisPatternPropertyId: str
    configFormulaPropertyId: str
    configResidualPropertyId: str
    configPredictionPropertyIds: 'list[str]' = []
    outputFolder: str
    crop: Optional[str] = Field(None)
