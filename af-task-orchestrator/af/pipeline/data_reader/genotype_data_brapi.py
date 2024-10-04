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
    VariantSet, AlleleMatrix,VariantsListResponse,
    Call,Variant, CallsSearchRequest,VariantsSearchRequest,
    VariantsListResponseResult,CallsListResponseResult,CallSetsListResponseResult, CallSet,
    Sample,SampleSearchRequest,SampleListResponse,SampleListResponseResult
)
from af.pipeline.data_reader.models.brapi.germplasm import (
    GermplasmSearchRequest, GermplasmListResponse, Germplasm, GermplasmListResponseResult
)

from af.pipeline.pandasutil import df_keep_columns
from pydantic import ValidationError

GET_VARIANT_SETS_URL = "/variantsets"
POST_SEARCH_CALLSETS_URL = "/search/germplasm"
GET_SEARCH_CALLSETS_URL = "/search/callsets"
GET_SEARCH_ALLELEMATRIX_URL = "/search/allelematrix"
POST_SEARCH_ALLELEMATRIX_URL="/search/allelematrix"
GET_SEARCH_CALLS_URL = "/search/calls"
POST_SEARCH_VARIANTS_URL = "/search/variants"
POST_SEARCH_GERMPLASM_URL = "/search/germplasm"

def getGermplasmId(g:Germplasm) -> str:
    return g.germplasmDbId

def getVariantDbId(v:Variant) -> str:
    return v.variantDbId

class GenotypeDataBrapi(GenotypeData):

    brapi_list_page_size = 1000
    
    #JDLS - note, this only works with one study ID at a time
    def get_germplasm(self, studyDbIds:'list[str]') -> 'list[Germplasm]':
        filters = GermplasmSearchRequest(studyDbIds=studyDbIds)
        
        api_response = self.post(endpoint=POST_SEARCH_GERMPLASM_URL,json=filters.dict())

        if not api_response.is_success:
            print(api_response.body) # JDLS - leaving this for diagnostics. Sorry if this clutters your output
            raise DataReaderException(api_response.error)
        
        brapi_response:GermplasmListResponseResult = GermplasmListResponseResult(**api_response.body["result"])

        return brapi_response.data
        
    
    def get_variant(self, studyDbIds:'list[str]' = None,variantDbIds:'list[str]'=None, variantSetDbIds:'list[str]'=None) ->'list[Variant]':  #TODO - rename to post variant -JDLS
        filters = VariantsSearchRequest(variantDbIds=variantDbIds, studyNames=studyDbIds,variantSetDbIds=variantSetDbIds)#JDLS - studyNames instead of StudyIds might make it work?

        api_response = self.post(endpoint=POST_SEARCH_VARIANTS_URL,json=filters.dict())

        if not api_response.is_success:
            raise DataReaderException(api_response.error)
        
        if api_response.http_status is None:
            raise DataReaderException(api_response.error)
        
        if api_response.http_status < 200 | api_response.http_status >= 300:
            raise DataReaderException(api_response.error)

        response = VariantsListResponse(**api_response.body)
        brapi_response:VariantsListResponseResult = response.result#VariantsListResponseResult(**api_response.body["result"])
        totalPages=1
        #print(f"Variant Response metadata was {response.metadata}")
        if( response.metadata is not None and 
            response.metadata.pagination is not None and 
            response.metadata.pagination.totalPages is not None and 
            (response.metadata.pagination.totalPages > 1)):
            totalPages = response.metadata.pagination.totalPages
        fullresponse = brapi_response.data
        page=1
        while(page < totalPages): #TODO - any error handling of subsequent calls - JDLS
            filters.page=page #If there's 2 pages, the pages are 0 and 1. Trust me, this math maths - JDLS
            page=page+1
            api_response = self.post(endpoint=POST_SEARCH_VARIANTS_URL,json=filters.dict())
            next_response:VariantsListResponseResult = response.result#VariantsListResponseResult(**api_response.body["result"])
            #print(f"Variant page {page} had {len(brapi_response.data)} elements, adding to {len(fullresponse)} existing elements")
            fullresponse+=next_response.data
        return fullresponse
    
    def get_call(self, studyDbIds:'list[str]',callSetDbIds:'list[str]'=None) -> 'list[Call]':
        
        filters = CallsSearchRequest(callSetDbIds=callSetDbIds,studyDbIds=studyDbIds)

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
    
    #Returns all 
    def get_variantsets(self, studyDbIds: 'list[str]' = None) -> 'list[VariantSet]':
        filters = VariantSetsSearchRequest(studyDbIds=studyDbIds)#JDLS - why was this callsetDbIds? 

        api_response = self.get(endpoint=GET_VARIANT_SETS_URL, params=filters.dict())

        if not api_response.is_success:
         raise DataReaderException(api_response.error)

        brapi_response:VariantSetsListResponseResult = VariantSetsListResponseResult(**api_response.body["result"])
        #print(f"Study: {studyDbIds} || VariantSets: {brapi_response.data}")#Todo - debugging
        return brapi_response.data
    
    def get_search_callsets(self, id, page: int = 0) -> ApiResponse:
        
        if page == 0:
            api_response = self.get(endpoint=GET_SEARCH_CALLSETS_URL + "/" + id)
        else:
            api_response = self.get(endpoint=GET_SEARCH_CALLSETS_URL + "/" + id, params={"pageSize": page})

        if not api_response.is_success:
            raise DataReaderException(api_response.error)
        
        return api_response

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
    
    def get_search_allelematrix_all(self, germplasmDbIds: list = None, sampleDbIds:list = None,dataMatrixNames:list=None, variantSetDbIds:list=None,
                                 expandHomozygotes:bool=None) -> 'list[AlleleMatrix]':#list[str]
        ret = []

        # do first post to search
        filters = AlleleMatrixSearchRequest(dataMatrixNames=dataMatrixNames,expandHomozygotes=expandHomozygotes,germplasmDbIds=germplasmDbIds,
                                            sampleDbIds=sampleDbIds,variantSetDbIds=variantSetDbIds,dataMatrixAbbreviations=["GT"])
        api_response:ApiResponse = self.get(endpoint=GET_SEARCH_ALLELEMATRIX_URL, params=filters.dict())
        
        if not api_response.is_success:
            raise DataReaderException(api_response.error)

        #     if api_response.http_status != 200:
     #       raise DataReaderException(api_response.error)

        brapi_response = AlleleMatrixResponse(**api_response.body)
        ret.append(brapi_response.result) #TODO - Multiple response matrices makes this pass awkward

        #This call shouldn't paginate, so this should occur rarely - JDLS
        #Ignore any pagination counts or reps
        return ret 

    
    def post_search_allelematrix(self, germplasmDbIds: list = None, sampleDbIds:list = None,dataMatrixNames:list=None, studyDbIds:list=None, variantSetDbIds:list=None, variantDbIds:list=None,
                                 expandHomozygotes:bool=None) -> 'list[AlleleMatrix]':#list[str]
        ##For now, lets just assume the unadorned get works - JDLS #Terriblehack And it didn't work -JDLS again
       # return GenotypeDataBrapi.get_search_allelematrix_all(self=self,germplasmDbIds=germplasmDbIds,sampleDbIds=sampleDbIds,dataMatrixNames=dataMatrixNames,variantSetDbIds=variantSetDbIds,expandHomozygotes=expandHomozygotes)
        ret = []

        getId = ""
    
        # do first post to search
        #JDLS terriblehack 
        
        #if(studyDbIds is not None):
        #    germplasms=self.get_germplasm(studyDbIds)
        #    germplasmDbIds=list(map(getGermplasmId,germplasms))
        #    print(f"Germplasm Ids: {germplasmDbIds[:10]}")
        filters = AlleleMatrixSearchRequest(dataMatrixNames=dataMatrixNames,expandHomozygotes=expandHomozygotes,germplasmDbIds=germplasmDbIds,
                                            sampleDbIds=sampleDbIds,variantSetDbIds=variantSetDbIds, variantDbIds=variantDbIds, dataMatrixAbbreviations=["GT"])
        api_response:ApiResponse = self.post(endpoint=POST_SEARCH_ALLELEMATRIX_URL, json=filters.dict())# or is it params=filters.dict() ? -JDLS
        
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
        

        pageNum = 0
        if(brapi_response.metadata.pagination is None or brapi_response.metadata.pagination.totalPages is None):
            totalPages=1
        else: totalPages = brapi_response.metadata.pagination.totalPages
        #This call shouldn't paginate, so this should occur rarely - JDLS
        ret.append(brapi_response.result) #We already got the first one
        while pageNum < (totalPages - 1):
            pageNum = pageNum + 1
            filters = AlleleMatrixSearchRequest(
                germplasmDbIds=germplasmDbIds, pageSize=self.brapi_list_page_size, page=pageNum
            )

            if paginationCalls == "post":
                filters.page = pageNum
                api_response = self.post(endpoint=POST_SEARCH_ALLELEMATRIX_URL, params=filters.dict())

                brapi_response = AlleleMatrixResponse(**api_response.body)
                ret.append(brapi_response.result) #TODO - Multiple response matrices makes this pass awkward
            elif paginationCalls == "get":
                api_response = self.get_search_allelematrix(getId, pageNum)

                brapi_response = AlleleMatrixResponse(**api_response.body)
                ret.append(brapi_response.result) #TODO - Multiple response matrices makes this pass awkward

            if not api_response.is_success:
                raise DataReaderException(api_response.error)

        return ret 
    
    def get_search_allelematrix(self, c_id, page: int = 0) -> ApiResponse:

        if page == 0:
            api_response = self.get(endpoint=GET_SEARCH_ALLELEMATRIX_URL + "/" + c_id)
        else:
            api_response = self.get(endpoint=GET_SEARCH_ALLELEMATRIX_URL + "/" + c_id, params={"pageSize": page})

        if not api_response.is_success:
            raise DataReaderException(api_response.error)

        return api_response