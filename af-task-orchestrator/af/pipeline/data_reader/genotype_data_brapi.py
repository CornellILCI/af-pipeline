import pandas as pd
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.data_reader.models import Occurrence
from af.pipeline.data_reader.models.api_response import ApiResponse
from af.pipeline.data_reader.models.brapi.core import BaseListResponse, Study
from af.pipeline.data_reader.models.brapi.genotyping import VariantSetRequest, VariantSetsListResponseResult, CallSetsSearchRequest, CallSetResponse, CallSetsListResponse, Field202AcceptedSearchResponse
from af.pipeline.data_reader.genotype_data import GenotypeData
from af.pipeline.pandasutil import df_keep_columns
from pydantic import ValidationError
from typing import Any, Dict, List, Optional

GET_VARIANT_SETS_URL = "/variantsets"
POST_SEARCH_CALLSETS_URL = "/search/germplasm"
GET_SEARCH_CALLSETS_URL = "/search/germplasm"


class GenotypeDataBrapi(GenotypeData):

    brapi_list_page_size = 1000

    def get_search_callsets(self, id) -> ApiResponse:

        api_response = self.get(endpoint=GET_SEARCH_CALLSETS_URL+"/"+id)

        if not api_response.is_success:
            raise DataReaderException(api_response.error)

        return api_response

    def get_variantsets(self, studyDbIds: list[str] = None) -> tuple:

        for studyDbId in studyDbIds:
            filters = VariantSetRequest(
                callSetDbId=studyDbId                
            )

            api_response = self.get(endpoint=GET_VARIANT_SETS_URL, params=filters.dict())

            if not api_response.is_success:
                raise DataReaderException(api_response.error)

            brapi_response = VariantSetsListResponseResult(**api_response.body['result'])

            
        


        return "",""

    def post_search_callsets(self, germplasmDbIds: list[str] = None) -> tuple :
        

        # do first post to search 
        filters = CallSetsSearchRequest(
            germplasmDbIds = germplasmDbIds
        )
        api_response = self.post(endpoint=POST_SEARCH_CALLSETS_URL, params=filters.dict())

        if not api_response.is_success:
            raise DataReaderException(api_response.error)

        if api_response.http_status == 202:
            
            response = api_response.http_status
            while response == 202:
                brapi_response = Field202AcceptedSearchResponse(**api_response.body)
                api_response = self.get_search_callsets(brapi_response.result.searchResultsDbId)
                response = api_response.http_status

        if api_response.http_status != 200:
            raise DataReaderException(api_response.error)
            
        brapi_response = CallSetResponse(**api_response.body)
            

        #if response is

        

        

        pageNum = 0
        totalPages = 0

        while pageNum == 0 or (pageNum < totalPages):
            filters = CallSetsSearchRequest(
                germplasmDbIds = germplasmDbIds,
                pageSize=self.brapi_list_page_size,
                page=pageNum
            )

            
            api_response = self.post(endpoint=POST_SEARCH_CALLSETS_URL, params=filters.dict())

            if not api_response.is_success:
                raise DataReaderException(api_response.error)

            


        return "",""


