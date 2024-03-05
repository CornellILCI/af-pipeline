import json
from typing import Any, Dict, List, Optional

import pandas as pd
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.data_reader.genotype_data import GenotypeData
from af.pipeline.data_reader.models.api_response import ApiResponse
from af.pipeline.data_reader.models.brapi.genotyping import (
    CallSetResponse,
    CallSetsListResponse,
    CallSetsSearchRequest,
    Field202AcceptedSearchResponse,
    VariantSetsListResponseResult,
    VariantSetsSearchRequest,
    VariantSetsExtractRequest,
    AlleleMatrixSearchRequest,
    AlleleMatrixResponse,
    AlleleMatrixDataMatrices,
    VariantSet, AlleleMatrix,
    Call,Variant, CallsSearchRequest,VariantsSearchRequest,
    VariantsListResponseResult,CallsListResponseResult,CallSetsListResponseResult, CallSet,
    Sample,SampleSearchRequest,SampleListResponse,SampleListResponseResult
)
from af.pipeline.pandasutil import df_keep_columns
from pydantic import ValidationError

GET_VARIANT_SETS_URL = "/variantsets"
POST_SEARCH_CALLSETS_URL = "/search/germplasm"
GET_SEARCH_CALLSETS_URL = "/search/callsets"
GET_SEARCH_ALLELEMATRIX_URL = "/search/allelematrix"
POST_SEARCH_ALLELEMATRIX_URL="/search/allelematrix"
GET_SEARCH_CALLS_URL = "/search/calls"
GET_SEARCH_VARIANTS_URL = "/search/variants"

class GenotypeDataBrapi(GenotypeData):

    brapi_list_page_size = 1000
    
    def get_variant(self, variantDbIds:'list[str]') ->'list[Variant]':
        for studyDbId in studyDbIds:
            filters = VariantsSearchRequest(variantDbIds=variantDbIds)

            api_response = self.get(endpoint=GET_SEARCH_VARIANTS_URL, params=filters.dict())

            if not api_response.is_success:
                raise DataReaderException(api_response.error)

            brapi_response:VariantsListResponseResult = VariantsListResponseResult(**api_response.body["result"])

        return brapi_response.data
    
    def get_call(self, callSetDbIds:'list[str]') -> 'list[Call]':
        
        filters = CallsSearchRequest(callSetDbIds=callSetDbIds)

        api_response = self.get(endpoint=GET_SEARCH_CALLS_URL, params=filters.dict())

        if not api_response.is_success:
            raise DataReaderException(api_response.error)

        brapi_response:CallsListResponseResult = CallsListResponseResult(**api_response.body["result"])

        return brapi_response.data

    def get_callsets(self, callSetDbIds:'list[str]') -> 'list[CallSet]':
        filters = CallSetsSearchRequest(callSetDbIds=callSetDbIds)
        api_response = self.get(endpoint=GET_SEARCH_CALLSETS_URL ,params=filters.dict())
        
        if not api_response.is_success:
            raise DataReaderException(api_response.error)
        
        brapi_response:CallSetsListResponseResult = CallSetsListResponseResult(**api_response.body["result"])

        return brapi_response.data
    
    def get_samples(self, sampleDbIds:'list[str]') -> 'list[Sample]':
        filters = SampleSearchRequest(sampleDbIds=sampleDbIds)
        api_response = self.get(endpoint=GET_SEARCH_SAMPLE_URL, params=filters.dict())
        
        if not api_response.is_success:
            raise DataReaderException(api_response.error)
        
        brapi_response:SampleListResponseResult = SampleListResponseResult(**api_response.body["result"])

        return brapi_response.data
    

    def get_variantsets(self, studyDbIds: list = None) -> 'list[VariantSet]':

        for studyDbId in studyDbIds:
            filters = VariantSetsSearchRequest(callSetDbId=studyDbId)

            api_response = self.get(endpoint=GET_VARIANT_SETS_URL, params=filters.dict())

            if not api_response.is_success:
                raise DataReaderException(api_response.error)

            brapi_response:VariantSetsListResponseResult = VariantSetsListResponseResult(**api_response.body["result"])

        return brapi_response.data

    def post_search_callsets(self, germplasmDbIds: list = None) -> list: #list[str]
        ret = []

        getId = ""
        # do first post to search
        filters = CallSetsSearchRequest(germplasmDbIds=germplasmDbIds)
        api_response = self.post(endpoint=POST_SEARCH_CALLSETS_URL, params=filters.dict())
        paginationCalls = "post"
        if not api_response.is_success:
            raise DataReaderException(api_response.error)

        if api_response.http_status == 202:

            response = api_response.http_status
            while response == 202:
                brapi_response = Field202AcceptedSearchResponse(**api_response.body)
                getId = brapi_response.result.searchResultsDbId
                api_response = self.get_search_callsets(getId)
                paginationCalls = "get"
                response = api_response.http_status

        if api_response.http_status != 200:
            raise DataReaderException(api_response.error)

        brapi_response = CallSetsListResponse(**api_response.body)
        ret.append(brapi_response.result.data)

        pageNum = 0
        totalPages = brapi_response.metadata.pagination.totalPages

        while pageNum < (totalPages - 1):
            pageNum = pageNum + 1
            filters = CallSetsSearchRequest(
                germplasmDbIds=germplasmDbIds, pageSize=self.brapi_list_page_size, page=pageNum
            )

            if paginationCalls == "post":
                filters.page = pageNum
                api_response = self.post(endpoint=POST_SEARCH_CALLSETS_URL, params=filters.dict())

                brapi_response = CallSetsListResponse(**api_response.body)
                ret.append(brapi_response.result.data)
            elif paginationCalls == "get":
                api_response = self.get_search_callsets(getId, pageNum)

                brapi_response = CallSetsListResponse(**api_response.body)
                ret.append(brapi_response.result.data)

            if not api_response.is_success:
                raise DataReaderException(api_response.error)

        return ret 
    
    def post_search_allelematrix(self, germplasmDbIds: list = None, sampleDbIds:list = None,dataMatrixNames:list=None, variantSetDbIds:list=None,
                                 expandHomozygotes:bool=None) -> 'list[AlleleMatrix]':#list[str]
        ret = []

        getId = ""
        # do first post to search
        filters = AlleleMatrixSearchRequest(dataMatrixNames=dataMatrixNames,expandHomozygotes=expandHomozygotes,germplasmDbIds=germplasmDbIds,
                                            sampleDbIds=sampleDbIds,variantSetDbIds=variantSetDbIds,dataMatrixAbbreviations="GT")
        api_response = self.post(endpoint=POST_SEARCH_CALLSETS_URL, params=filters.dict())
        paginationCalls = "post"
        if not api_response.is_success:
            raise DataReaderException(api_response.error)

        if api_response.http_status == 202:

            response = api_response.http_status
            while response == 202:
                brapi_response = Field202AcceptedSearchResponse(**api_response.body)
                getId = brapi_response.result.searchResultsDbId
                api_response = self.get_search_allelematrix(getId)
                paginationCalls = "get"
                response = api_response.http_status

        if api_response.http_status != 200:
            raise DataReaderException(api_response.error)

        brapi_response = AlleleMatrixResponse(**api_response.body)
        ret.append(brapi_response.result) #TODO - Multiple response matrices makes this pass awkward

        pageNum = 0
        totalPages = brapi_response.metadata.pagination.totalPages

        while pageNum < (totalPages - 1):
            pageNum = pageNum + 1
            filters = AlleleMatrixSearchRequest(
                germplasmDbIds=germplasmDbIds, pageSize=self.brapi_list_page_size, page=pageNum
            )

            if paginationCalls == "post":
                filters.page = pageNum
                api_response = self.post(endpoint=POST_SEARCH_CALLSETS_URL, params=filters.dict())

                brapi_response = AlleleMatrixResponse(**api_response.body)
                ret.append(brapi_response.result) #TODO - Multiple response matrices makes this pass awkward
            elif paginationCalls == "get":
                api_response = self.get_search_allelematrix(getId, pageNum)

                brapi_response = AlleleMatrixResponse(**api_response.body)
                ret.append(brapi_response.result) #TODO - Multiple response matrices makes this pass awkward

            if not api_response.is_success:
                raise DataReaderException(api_response.error)

        return ret 
    
    def get_search_allelematrix(self, c_id, page: int = 0) -> 'list[AlleleMatrix]':

        if page == 0:
            api_response = self.get(endpoint=GET_SEARCH_ALLELEMATRIX_URL + "/" + c_id)
        else:
            api_response = self.get(endpoint=GET_SEARCH_ALLELEMATRIX_URL + "/" + c_id, params={"pageSize": page})

        if not api_response.is_success:
            raise DataReaderException(api_response.error)
        
        response:AlleleMatrixResponse = AlleleMatrixResponse(**api_response.body)
        dataMatrices:list[AlleleMatrixDataMatrices] = response.result.dataMatrices

        return dataMatrices