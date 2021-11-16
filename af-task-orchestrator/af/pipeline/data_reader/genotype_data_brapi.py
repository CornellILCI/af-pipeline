import json
from typing import Any, Dict, List, Optional

import pandas as pd
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.data_reader.genotype_data import GenotypeData
from af.pipeline.data_reader.models import Occurrence
from af.pipeline.data_reader.models.api_response import ApiResponse
from af.pipeline.data_reader.models.brapi.core import BaseListResponse, Study
from af.pipeline.data_reader.models.brapi.genotyping import (
    CallSetResponse,
    CallSetsListResponse,
    CallSetsSearchRequest,
    Field202AcceptedSearchResponse,
    VariantSetRequest,
    VariantSetsListResponseResult,
)
from af.pipeline.pandasutil import df_keep_columns
from pydantic import ValidationError

GET_VARIANT_SETS_URL = "/variantsets"
POST_SEARCH_CALLSETS_URL = "/search/germplasm"
GET_SEARCH_CALLSETS_URL = "/search/germplasm"


class GenotypeDataBrapi(GenotypeData):

    brapi_list_page_size = 1000

    def get_search_callsets(self, id, page: int = 0) -> ApiResponse:

        if page == 0:
            api_response = self.get(endpoint=GET_SEARCH_CALLSETS_URL + "/" + id)
        else:
            api_response = self.get(endpoint=GET_SEARCH_CALLSETS_URL + "/" + id, params={"pageSize": page})

        if not api_response.is_success:
            raise DataReaderException(api_response.error)

        return api_response

    def get_variantsets(self, studyDbIds: list[str] = None) -> tuple:

        for studyDbId in studyDbIds:
            filters = VariantSetRequest(callSetDbId=studyDbId)

            api_response = self.get(endpoint=GET_VARIANT_SETS_URL, params=filters.dict())

            if not api_response.is_success:
                raise DataReaderException(api_response.error)

            brapi_response = VariantSetsListResponseResult(**api_response.body["result"])

        return "", ""

    def post_search_callsets(self, germplasmDbIds: list[str] = None) -> list:
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
