import json
from typing import List

import pandas as pd
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.data_reader.models import Occurrence
from af.pipeline.data_reader.models.brapi.core import BaseListResponse, Study, TableResponse
from af.pipeline.data_reader.models.brapi.germplasm import Germplasm
from af.pipeline.data_reader.models.brapi.phenotyping import (
    ObservationUnitQueryParams,
    ObservationQueryParams,
    ObservationUnitsSearchRequestDto,
)
from af.pipeline.data_reader.phenotype_data import PhenotypeData
from af.pipeline.pandasutil import df_keep_columns
from pydantic import BaseModel, ValidationError, parse_obj_as

# all urls are set here
GET_OBSERVATION_UNITS_URL = "/observationunits"

GET_OBSERVATIONS_URL = "/observations"

GET_STUDIES_BY_ID_URL = "/studies/{studyDbId}"  # noqa:

POST_SEARCH_OBSERVATION_UNITS_URL = "/search/observationunits"

GET_OBSERVATION_UNITS_SEARCH_RESULTS_URL = "/search/observationunits/{searchResultsDbId}"


class PhenotypeDataBrapi(PhenotypeData):
    """Reads phenotype data from a brapi ebs data source."""

    # TODO: termporary patching where same name mapping can be avoided by adding a logic in 
    # code
    plots_api_fields_to_local_fields = {
        "observationUnitDbId": "observationUnitDbId",
        "germplasmDbId": "germplasmDbId",
        "studyDbId": "studyDbId",
        "trialDbId": "trialDbId",
        "locationDbId": "locationDbId",
        "observationUnitPosition.positionCoordinateX": "positionCoordinateX",
        "observationUnitPosition.positionCoordinateY": "positionCoordinateY",
    }

    plot_measurements_api_fields_to_local_fields = {
        "observationUnitDbId": "observationUnitDbId",
        "observationVariableDbId": "trait_id",
        "value": "trait_value",
    }

    brapi_list_page_size = 1000

    def get_plots_from_search(self, exp_id: str = None) -> pd.DataFrame:

        # first POST to /bmsapi/{crop}/brapi/v2/search/observationunits
        observation_units_filters = ObservationUnitsSearchRequestDto(studyDbIds=[exp_id], observationLevel="PLOT")

        post_response = self.post(endpoint=GET_POST_OBSERVATION_UNITS_URL_BMS_V2, json=observation_units_filters.dict())
        if not post_response.is_success:
            raise DataReaderException(post_response.error)

        observation_units_id = post_response.body["result"]["searchResultsDbId"]
        plots_data = []

        columns_path = [
            "observationUnitDbId",
            "locationDbId",
            "studyDbId",
            "trialDbId",
            "germplasmDbId",
            ["observationUnitPosition", "positionCoordinateX"],
            ["observationUnitPosition", "positionCoordinateY"],
        ]
        page_num = 0

        get_more_plots = True
        # the loop goes here

        data = []

        dataframes = []

        while get_more_plots:

            observation_units_filters = ObservationUnitQueryParams(pageSize=self.brapi_list_page_size, page=page_num)
            get_response = self.get(endpoint=GET_POST_OBSERVATION_UNITS_URL_BMS_V2 + "/" + observation_units_id)

            if not get_response.is_success:
                raise DataReaderException(get_response.error)

            brapi_response = BaseListResponse(**get_response.body)

            plots_data = brapi_response.result.data

            if len(plots_data) == 0 and page_num == 0:
                columns = list(self.plots_api_fields_to_local_fields.values())
                columns.append("plot_qc")
                return pd.DataFrame(columns=columns)

            # build a json object with all the info

            rows = []
            for x in get_response.body["result"]["data"]:
                temp = {}

                for y in x["observationUnitPosition"]["observationLevelRelationships"]:
                    if y["levelName"] == "PLOT":
                        temp["Plot"] = y["levelCode"]
                    if y["levelName"] == "REP":
                        temp["Rep"] = y["levelCode"]

                if x["observationUnitPosition"]["positionCoordinateXType"] == "GRID_COL":
                    temp["Col"] = x["observationUnitPosition"]["positionCoordinateX"]
                elif x["observationUnitPosition"]["positionCoordinateXType"] == "GRID_ROW":
                    temp["Row"] = x["observationUnitPosition"]["positionCoordinateX"]

                if x["observationUnitPosition"]["positionCoordinateYType"] == "GRID_COL":
                    temp["Col"] = x["observationUnitPosition"]["positionCoordinateY"]
                elif x["observationUnitPosition"]["positionCoordinateYType"] == "GRID_ROW":
                    temp["Row"] = x["observationUnitPosition"]["positionCoordinateY"]

                for y in x["observations"]:
                    temp[y["observationVariableName"]] = y["value"]

                rows.append(temp)

            ndf = pd.json_normalize(rows)

            dataframes.append(ndf)

            if page_num < get_response.body["metadata"]["pagination"]["totalPages"]:
                page_num += 1
            else:
                get_more_plots = False
        ret = pd.concat(dataframes, ignore_index=True)
        return ret

    def get_plots(self, occurrence_id: str = None) -> pd.DataFrame:
        """Implementation for BMS get_plots."""

        plots_data = []

        page_num = 0

        observation_units_filters = ObservationUnitsSearchRequestDto(
            studyDbIds=[occurrence_id], observationLevel="PLOT"
        )

        post_response = self.post(
            endpoint=POST_SEARCH_OBSERVATION_UNITS_URL, json=observation_units_filters.dict()
        )
        if not post_response.is_success:
            raise DataReaderException(post_response.error)

        search_result_id = post_response.body["result"]["searchResultsDbId"]

        observation_units_filters = ObservationUnitQueryParams(pageSize=self.brapi_list_page_size)

        while len(plots_data) >= self.brapi_list_page_size or page_num == 0:

            observation_units_filters.page = page_num

            results_endpoint = GET_OBSERVATION_UNITS_SEARCH_RESULTS_URL.format(searchResultsDbId=search_result_id)

            api_response = self.get(endpoint=results_endpoint, params=observation_units_filters.dict())

            if not api_response.is_success:
                raise DataReaderException(api_response.error)

            brapi_response = BaseListResponse(**api_response.body)

            plots_data = brapi_response.result.data

            if len(plots_data) == 0 and page_num == 0:
                columns = list(self.plots_api_fields_to_local_fields.values())
                columns.append("plot_qc")
                return pd.DataFrame(columns=columns)

            # paths to normalize json data to flat columns
            columns_path = [
                "observationUnitDbId",
                "locationDbId",
                "studyDbId",
                "trialDbId",
                "germplasmDbId",
                ["observationUnitPosition", "positionCoordinateX"],
                ["observationUnitPosition", "positionCoordinateY"],
            ]

            # list record path to normalze
            list_record_path = ["observationUnitPosition", "observationLevelRelationships"]

            # this dataframe will have observation level array as seperate rows
            plots_unpivoted = pd.json_normalize(
                plots_data,
                record_path=list_record_path,
                meta=columns_path,
            )

            plots_observation_levels_pivoted = plots_unpivoted.pivot(
                index="observationUnitDbId", columns="levelName", values="levelCode"
            )

            plots_observation_levels_droped = (
                plots_unpivoted.drop(columns=["levelOrder", "levelCode", "levelName"]).drop_duplicates().reset_index()
            )

            plots_page = plots_observation_levels_droped.join(
                plots_observation_levels_pivoted, on="observationUnitDbId"
            )

            # keep only local field columns
            plots_page = df_keep_columns(plots_page, self.plots_api_fields_to_local_fields.keys())

            # since plot_qc not defined in brapi spec, set default value "G"
            plots_page["plot_qc"] = "G"

            if page_num == 0:
                plots = plots_page
            else:
                plots = plots.append(plots_page)

            # to get next page
            page_num += 1

        # rename dataframe column with local field names
        plots.rename(columns=self.plots_api_fields_to_local_fields, inplace=True)

        return plots.astype(str)

    def get_plot_measurements(self, occurrence_id: str = None, trait_id: str = None) -> pd.DataFrame:

        plot_measurements_data = []

        page_num = 0

        observations_filters = ObservationQueryParams(
            studyDbId=occurrence_id, observationVariableDbId=trait_id, pageSize=1000
        )
        
        while len(plot_measurements_data) >= self.brapi_list_page_size or page_num == 0:

            observations_filters.page = page_num

            api_response = self.get(endpoint=GET_OBSERVATIONS_URL, params=observations_filters.dict())

            if not api_response.is_success:
                raise DataReaderException(api_response.error)

            brapi_response = BaseListResponse(**api_response.body)

            plot_measurements_data = brapi_response.result.data

            plot_measurements_page = pd.DataFrame(plot_measurements_data)

            if page_num == 0:
                plot_measurements = plot_measurements_page
            else:
                plot_measurements = plot_measurements.append(plot_measurements_page)

            page_num += 1

        # keep only local field columns
        plot_measurements = df_keep_columns(plot_measurements, self.plot_measurements_api_fields_to_local_fields.keys())

        # rename columns to local field names
        plot_measurements = plot_measurements.rename(
            columns=self.plot_measurements_api_fields_to_local_fields,
        )

        # trait_qc not part of brapi spec, so set to default value
        plot_measurements["trait_qc"] = "G"

        return plot_measurements.astype(str)

    def get_occurrence(self, occurrence_id: int = None):

        studies_url = GET_STUDIES_BY_ID_URL.format(studyDbId=occurrence_id)
        api_response = self.get(endpoint=studies_url)

        if not api_response.is_success:
            raise DataReaderException(api_response.error)

        result = api_response.body["result"]

        if result is None:
            raise DataReaderException("Occurrence is not found")

        # load it to model to make sure required fields are found
        try:
            _study = Study(**result)
        except ValidationError as e:
            raise DataReaderException(str(e))

        return Occurrence(
            occurrence_id=_study.studyDbId,
            occurrence_name=_study.studyName,
            experiment_id=_study.trialDbId,
            experiment_name=_study.trialName,
            location_id=_study.locationDbId,
            location=_study.locationName,
        )

    def get_experiment(self, experiment_id: int = None):
        raise NotImplementedError

    def get_trait(self, trait_id: int = None):
        raise NotImplementedError

    def search_germplasm(self, germplasm_search_ids: list[str]):

        search_query = {"germplasmDbIds": germplasm_search_ids}

        search_germplasm_response = self.post(endpoint="/search/germplasm/", json=search_query)

        if not search_germplasm_response.is_success:
            raise DataReaderException(search_germplasm.error)  # TODO: search_germplasm is undefined here

        if search_germplasm_response.body is None:
            raise DataReaderException("Germplasms are not found")

        if search_germplasm_response.http_status == 202:

            search_germplasm_dbid = search_germplasm_response.body["result"]["searchResultDbId"]

            germplasm_url = GET_GERMPLASM_BY_DB_ID.format(searchResultDbId=search_germplasm_dbid)

            get_germplasm = self.get(endpoint=germplasm_url)
            germplasm_list = parse_obj_as(list[Germplasm], get_germplasm.body["result"]["data"])

            return germplasm_list

        if search_germplasm_response.http_status == 200:

            germplasm_list = parse_obj_as(list[Germplasm], search_germplasm_response.body["result"]["data"])
            return germplasm_list

        if not get_germplasm.is_success:
            raise DataReaderException(search_germplasm.error)  # TODO: search_germplasm is undefined here

        if get_germplasm.body is None:
            raise DataReaderException("Germplasms are not found")
