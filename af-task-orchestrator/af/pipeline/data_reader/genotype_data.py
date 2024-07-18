from abc import ABC, abstractmethod

import pandas as pd
from af.pipeline.data_reader.data_reader import DataReader
from af.pipeline.data_reader.models import Experiment, Occurrence, Trait
from af.pipeline.data_reader.models.api_response import ApiResponse
from af.pipeline.data_reader.models.brapi.genotyping import VariantSet, AlleleMatrixDataMatrices, AlleleMatrix, Variant, Call, Sample, CallSet
from af.pipeline.data_reader.models.brapi.germplasm import Germplasm

class GenotypeData(ABC, DataReader):
    """Interface for reading genotype data from different kinds of
    data sources
    """
    @abstractmethod
    def get_search_callsets(self, id, page: int = 0) -> ApiResponse:
        pass
    
    @abstractmethod
    def get_variantsets(self, studyDbIds: list = None) -> 'list[VariantSet]':
        pass
    @abstractmethod    
    def get_variant(self,  studyDbIds:'list[str]'=None,variantDbIds:'list[str]'=None, variantSetDbIds:'list[str]'=None) ->'list[Variant]':
        pass
    
    @abstractmethod
    def get_call(self, studyDbIds:'list[str]',callSetDbIds:'list[str]'=None) -> 'list[Call]':
        pass
    
    @abstractmethod
    def get_samples(self, sampleDbIds:'list[str]') -> 'list[Sample]':
        pass

    @abstractmethod
    def get_callsets(self, callSetDbIds:'list[str]') -> 'list[CallSet]':
        pass
    
    @abstractmethod
    def get_germplasm(self, studyDbIds:'list[str]') -> 'list[Germplasm]':
        pass
    
    @abstractmethod
    def post_search_callsets(self, germplasmDbIds: list = None) -> list:
        pass
    @abstractmethod
    def post_search_allelematrix(self,  germplasmDbIds: list = None, sampleDbIds:list = None,dataMatrixNames:list=None, studyDbIds:list=None, variantDbIds:list=None, 
                                 variantSetDbIds:list=None, expandHomozygotes:bool=None) -> 'list[AlleleMatrix]':
        pass
    @abstractmethod
    def get_search_allelematrix(self, germplasmDbIds: list = None, sampleDbIds:list = None,dataMatrixNames:list=None,studyDbIds:list=None, variantSetDbIds:list=None) -> list:
        pass
    