import pandas as pd
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.data_reader.models import Occurrence
from af.pipeline.data_reader.models.brapi.core import BaseListResponse, Study
from af.pipeline.data_reader.models.brapi.genotyping import VariantSetRequest, VariantSetsListResponseResult, CallSetsSearchRequest
from af.pipeline.data_reader.genotype_data import GenotypeData
from af.pipeline.pandasutil import df_keep_columns
from pydantic import ValidationError
from typing import Any, Dict, List, Optional

GET_VARIANT_SETS_URL = "/variantsets"
POST_SEARCH_CALLSETS_URL = "/search/germplasm"


class GenotypeDataBrapi(GenotypeData):

    brapi_list_page_size = 1000

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