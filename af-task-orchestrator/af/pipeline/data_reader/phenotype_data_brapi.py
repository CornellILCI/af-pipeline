import json
from typing import List

import pandas as pd
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.data_reader.models import Occurrence
from af.pipeline.data_reader.models.brapi.core import ListResponse, Study
from af.pipeline.data_reader.models.brapi.germplasm import Germplasm
from af.pipeline.data_reader.models.observation_unit import ObservationUnitQueryParams

from af.pipeline.data_reader.models.brapi.phenotyping import ObservationUnitSearchRequest, ObservationUnitLevel1,ObservationUnitListResponse, ObservationUnit, ObservationUnitLevelRelationship1, ObservationUnitListResponseResult, ObservationSearchRequest,ObservationListResponse



from af.pipeline.data_reader.models.brapi.genotyping import Sample, SampleListResponse, SampleSearchRequest

from af.pipeline.data_reader.phenotype_data import PhenotypeData
from af.pipeline.pandasutil import df_keep_columns
from pydantic import ValidationError, parse_obj_as

# all urls are set here
GET_OBSERVATION_UNITS_URL = "/observationunits"

GET_OBSERVATIONS_URL = "/observations"

GET_SEARCH_OBSERVATIONS_URL = "/search/observations"

GET_STUDIES_BY_ID_URL = "/studies/{studyDbId}"  # noqa:

POST_SEARCH_OBSERVATION_UNITS_URL = "/search/observationunits"

GET_OBSERVATION_UNITS_SEARCH_RESULTS_URL = "/search/observationunits/{searchResultsDbId}"

GET_SAMPLES_URL = "/samples"

POST_SAMPLES_URL = "/search/samples"

POST_SAMPLES_RESULTS_URL = "/search/samples/{searchResultDbId}"
    
#Debugging - prints the top couple lines of a dataframe
def printFirstLineOfDataframe(df:pd.DataFrame,dfName):
    df2 = df.head(4)
    print(f"DataFrame {dfName}")
    print(df2)
    return

#'flattens' an observation unit to a 'row' for every observation unit relationship, and if there are no relationship, adds a 'rep' of nothing. 
# This tries to replicate a bit of clever code using doubly nested column lists that no longer works - JDLS
# The caller then pulls out the observations it cares about, and deduplicates the resulting dataframe. The logic for what 'it cares about' should probably go into this function...
# in the next revamping pass
#Original had some problems with dataframe trying to 'flatten' the object. This 'flattens' the objects out in what I think is the same logic the old code used to do when it worked. -JDLS
def flattenObservationObject(obs:List[ObservationUnit]):
    output = list()
    for x in obs:
        oUP=x.observationUnitPosition;
        if (oUP.observationLevelRelationships is None): 
            oUP.observationLevelRelationships = list()
        if len(oUP.observationLevelRelationships) < 1: 
            y={"observationUnitDbId":x.observationUnitDbId,
            "germplasmDbId": x.germplasmDbId,
            "studyDbId": x.studyDbId,
            "trialDbId": x.trialDbId,
            "locationDbId": x.locationDbId,
            "observationUnitPosition":str(oUP.positionCoordinateX) + " " + str(oUP.positionCoordinateY),
            "positionCoordinateX":oUP.positionCoordinateX,
            "positionCoordinateY":oUP.positionCoordinateY,
            "levelName":"REP", #Just putting a blank 'rep' here for now
            "levelCode":None,
            "levelOrder":None,
            }
            output.append(y)        
        for relationship in oUP.observationLevelRelationships: 
            y={"observationUnitDbId":x.observationUnitDbId,
            "germplasmDbId": x.germplasmDbId,
            "studyDbId": x.studyDbId,
            "trialDbId": x.trialDbId,
            "locationDbId": x.locationDbId,
            "observationUnitPosition":str(oUP.positionCoordinateX) + " " + str(oUP.positionCoordinateY),
            "positionCoordinateX":oUP.positionCoordinateX,
            "positionCoordinateY":oUP.positionCoordinateY,
            "levelName":relationship.levelName,
            "levelCode":relationship.levelCode,
            "levelOrder":relationship.levelOrder,
            }
            output.append(y)
    return output

class PhenotypeDataBrapi(PhenotypeData):
    """Reads phenotype data from a brapi ebs data source."""

    # TODO: termporary patching where same name mapping can be avoided by adding a logic in 
    # code
    # TODO on the TODO: 'temporary'. api_to_local(*) needs to be reworked
    plots_api_fields_to_local_fields = {
        "observationUnitDbId": "observationUnitDbId",
        "germplasmDbId": "germplasmDbId",
        "studyDbId": "studyDbId",
        "trialDbId": "trialDbId",
        "locationDbId": "locationDbId",
        "positionCoordinateX": "positionCoordinateX",
        "positionCoordinateY": "positionCoordinateY",
        "REP": "replicate"
    }

    plot_measurements_api_fields_to_local_fields = {
        "observationUnitDbId": "observationUnitDbId",
        #"observationVariableDbId": "trait_id",
       # "value": "trait_value", JDLS - we're using pivot_table to pull the names the DB used for the traits
    }

    brapi_list_page_size = 1000

    def get_plots_from_search(self, exp_id: str = None) -> pd.DataFrame:

        # first POST to /bmsapi/{crop}/brapi/v2/search/observationunits
        observation_units_filters = ObservationUnitSearchRequest(studyDbIds=[exp_id], observationLevel="PLOT")

        post_response = self.post(endpoint=GET_POST_OBSERVATION_UNITS_URL_BMS_V2, json=observation_units_filters.dict()) #TODO: BMS name in the brapi? Glad this was never used
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
            get_response = self.get(endpoint=GET_POST_OBSERVATION_UNITS_URL_BMS_V2 + "/" + observation_units_id) #TODO: BMS name in the brapi? Glad this was never used

            if not get_response.is_success:
                raise DataReaderException(get_response.error)
 
            brapi_response = ObservationUnitListResponse(get_response.body)

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
        level:ObservationUnitLevel1=ObservationUnitLevel1(levelName="plot")
        observation_units_filters = ObservationUnitSearchRequest(
            studyDbIds=[occurrence_id], observationLevels=[level]
        )

        post_response = self.post(
            endpoint=POST_SEARCH_OBSERVATION_UNITS_URL, json=observation_units_filters.dict()
        )
        if not post_response.is_success:
            print(post_response.body)#Lets give the error to standard out as well - JDLS
            print(post_response.error)
            raise DataReaderException(post_response.error)

        search_result_id = post_response.body["result"]["searchResultsDbId"]

        observation_units_filters = ObservationUnitQueryParams(pageSize=self.brapi_list_page_size)

        while len(plots_data) >= self.brapi_list_page_size or page_num == 0:

            observation_units_filters.page = page_num

            results_endpoint = GET_OBSERVATION_UNITS_SEARCH_RESULTS_URL.format(searchResultsDbId=search_result_id)

            api_response = self.get(endpoint=results_endpoint, params=observation_units_filters.dict())

            if not api_response.is_success:
                raise DataReaderException(api_response.error)

            brapi_response = ObservationUnitListResponse(**api_response.body)#It's a list of observation units

            plots_data = brapi_response.result.data
            
            # build a json object with all the info
           

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
            
            new_plots_data=flattenObservationObject(plots_data) #Make into a proper flatish dictionary
            
            #printFirstLineOfDataframe(new_plots_data,'new_plots_data')
            
            # this dataframe will have observation level array as seperate rows
            new_columns_path=[
                "observationUnitDbId",
                "germplasmDbId",
                "studyDbId",
                "trialDbId",
                "locationDbId",
                "observationUnitPosition",
                "positionCoordinateX",
                "positionCoordinateY",
                "levelName",
                "levelCode",
                "levelOrder",
            ]
            
            new_plots_data_df = pd.DataFrame(data=new_plots_data,columns=new_columns_path)#,columns=columns_path);
            
            plots_unpivoted=new_plots_data_df
            plots_observation_levels_pivoted = plots_unpivoted.pivot(
                index="observationUnitDbId", columns="levelName", values="levelCode"  #columns = [[levelName]] was 'columns is the type of level name' aka plot, block, rep...deal with that tomorrow
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
                plots = pd.concat([plots,plots_page]) #was append - JDLS
                

            # to get next page
            page_num += 1

        # rename dataframe column with local field names
        plots.rename(columns=self.plots_api_fields_to_local_fields, inplace=True)

        #printFirstLineOfDataframe(plots,f'plots[{len(plots)}]') #GetPlots seems to be working - JDLS
        return plots.astype(str)

    def get_plot_measurements_list(self,occurrence_ids: list[str] = None, trait_ids:list[str] = None) -> pd.DataFrame:
        
        plot_measurements_data = []

        page_num = 0

        observations_filters = ObservationSearchRequest(
            studyDbIds=occurrence_ids,observationVariableDbIds=trait_ids, pageSize=1000
        )
        
        post_response = self.post(endpoint=GET_SEARCH_OBSERVATIONS_URL, json=observations_filters.dict())
        if not post_response.is_success:
            raise DataReaderException(post_response.error)

        request_id = post_response.body["result"]["searchResultsDbId"]
        page_num = 0

        get_more = True
        
        data = []
        while get_more:

            filters = ObservationSearchRequest(pageSize=self.brapi_list_page_size, page=page_num)
            get_response = self.get(endpoint=GET_SEARCH_OBSERVATIONS_URL + "/" + request_id, json=filters.dict())

            if not get_response.is_success:
                raise DataReaderException(get_response.error)
 
            brapi_response = ObservationListResponse(**get_response.body)        
        
        
            plot_measurements_data = brapi_response.result.data

            plot_measurements_page = pd.DataFrame(data=[obs.dict() for obs in plot_measurements_data])

            if page_num == 0:
                plot_measurements = plot_measurements_page
            else:
                plot_measurements = pd.concat([plot_measurements,plot_measurements_page])                       
            if page_num < brapi_response.metadata.pagination.totalPages:
                page_num += 1
            else:
                get_more = False

        #Taken from 'formatInputData', which munged it and ran it on a much larger dataset. Sorry future maintainer for breaking the containment
        #Pivot the traits so instead of having traitId as a column, each trait gets its own column    
            # From:
            #OVName  value
            #yield     37
            #height    6'2\
                #Note - ObservationVaraibleName might not be the greatest choice, but observationvariabledbid is the search term. We'll need the name later, though... So it saves a step
                #to do here... May kill multi-linqual support. Sorry - JDLS
                
        #printFirstLineOfDataframe(plot_measurements['observationUnitDbId','value','observationVariableName'],"plot_measurements_useful_columns")
        #plot_measurements.pivot(index='observationUnitDbId',values="value",columns="observationVariableName")#fill_value=config.UNIVERSAL_UNKNOWN)#TODO - index - every other column?
        #aggfunction -> take first value if there's duplicates.
        #TODO - why are there duplicates? JDLS
        
        plot_measurements=plot_measurements.pivot_table(index='observationUnitDbId',values="value",columns="observationVariableName",aggfunc='first', fill_value="NA")#fill_value=config.UNIVERSAL_UNKNOWN)#TODO - index - every other column?
        
         #printFirstLineOfDataframe(plot_measurements,f"plot_measurements_pivoted [{len(plot_measurements)}]")       

        plot_measurements=plot_measurements.reset_index()

        plot_measurements = plot_measurements.rename(columns={'observationVariableName':'observationUnitDbId'})
        plot_measurements = plot_measurements.drop_duplicates(keep='first',subset='observationUnitDbId') #Sometimes there's 4+ rows... confusing

        # keep only local field columns - already done in pivot
        #plot_measurements = df_keep_columns(plot_measurements, self.plot_measurements_api_fields_to_local_fields.keys())
        # rename columns to local field names
        plot_measurements = plot_measurements.rename(
            columns=self.plot_measurements_api_fields_to_local_fields,
        )
        
        # trait_qc not part of brapi spec, so set to default value
        plot_measurements["trait_qc"] = "G"
            

        return plot_measurements.astype(str)


        
    def get_plot_measurements(self, occurrence_id: str = None, trait_id: str = None) -> pd.DataFrame:

        plot_measurements_data = []

        page_num = 0

       # observations_filters = ObservationQueryParams(
        ##    studyDbId=occurrence_id, observationVariableDbId=trait_id, pageSize=1000
       # )
        observations_filters = ObservationSearchRequest(
            studyDbIds=[occurrence_id],observationVariableDbIds=[trait_id], pageSize=1000 #JDLS - don't we have a page.size config param now?
        )
        
        while len(plot_measurements_data) >= self.brapi_list_page_size or page_num == 0:

            observations_filters.page = page_num

            api_response = self.get(endpoint=GET_OBSERVATIONS_URL, params=observations_filters.dict())

            if not api_response.is_success:
                raise DataReaderException(api_response.error)

            brapi_response = ListResponse(**api_response.body)  

            plot_measurements_data = brapi_response.result.data

            plot_measurements_page = pd.DataFrame(plot_measurements_data)

            if page_num == 0:
                plot_measurements = plot_measurements_page
            else:
                plot_measurements = pd.concat([plot_measurements,plot_measurements_page])

            page_num += 1
            

        # keep only local field columns
        plot_measurements = df_keep_columns(plot_measurements, self.plot_measurements_api_fields_to_local_fields.keys())
        #printFirstLineOfDataframe(plot_measurements,'plot_measurements')
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

    def search_germplasm(self, germplasm_search_ids: list):

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
            germplasm_list = parse_obj_as('list[Germplasm]', get_germplasm.body["result"]["data"])

            return germplasm_list

        if search_germplasm_response.http_status == 200:

            germplasm_list = parse_obj_as('list[Germplasm]', search_germplasm_response.body["result"]["data"])
            return germplasm_list

        if not get_germplasm.is_success:
            raise DataReaderException(search_germplasm.error)  # TODO: search_germplasm is undefined here

        if get_germplasm.body is None:
            raise DataReaderException("Germplasms are not found")
        
        
        """Gets samples based on sample Ids, observation Ids, study Ids, or germplasm IDs, using BRAPIcalls
        """
    def get_samples(self, sample_ids: List[str]=None, observation_ids: List[str]=None , studyDbIds:List[str] = None, germplasmDbIds:List[str]=None) -> List[Sample]:
        sample_filters = SampleSearchRequest(sampleDbIds=sample_ids,observationUnitDbIds=observation_ids,studyDbIds=studyDbIds, germplasmDbIds=germplasmDbIds) #Nones are ignored, so this can do either or or both


        post_response = self.post(endpoint=POST_SAMPLES_URL, json=sample_filters.dict()) 
        if not post_response.is_success:
            raise DataReaderException(post_response.error)

        sample_request_id = post_response.body["result"]["searchResultsDbId"]
        page_num = 0

        get_more_samples = True
        
        data = []
        while get_more_samples:

            sample_filters = SampleSearchRequest(pageSize=self.brapi_list_page_size, page=page_num)  #-Unused?
            get_response = self.get(endpoint=POST_SAMPLES_URL + "/" + sample_request_id, json=sample_filters.dict() ) #Or postsamplesresultsurl

            if not get_response.is_success:
                raise DataReaderException(get_response.error)
 
            brapi_response = SampleListResponse(**get_response.body)
            
            samples_data = brapi_response.result.data
            
            data.extend(samples_data)
            
            if page_num < get_response.body["metadata"]["pagination"]["totalPages"]:
                page_num += 1
            else:
                get_more_samples = False

            
        return data
