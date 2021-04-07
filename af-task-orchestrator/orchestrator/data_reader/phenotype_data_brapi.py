import pandas as pd
from common import df_keep_columns
from data_reader.phenotype_data import PhenotypeData
from exceptions import DataReaderException
from models import Occurrence
from models.brapi.core import BaseListResponse, Study
from models.brapi.phenotyping import ObservationUnitQueryParams
from pydantic import ValidationError

GET_OBSERVATION_UNITS_URL = "/observationunits"

GET_OBSERVATIONS_URL = "/observations"

GET_STUDIES_BY_ID_URL = "/studies/{studyDbId}"


class PhenotypeDataBrapi(PhenotypeData):
    """Reads phenotype data from a brapi ebs data source."""

    plots_api_fields_to_local_fields = {
        "observationUnitDbId": "plot_id",
        "germplasmDbId": "entry_id",
        "studyDbId": "occurrence_id",
        "trialDbId": "experiment_id",
        "locationDbId": "location_id",
        "observationUnitPosition.positionCoordinateX": "pa_x",
        "observationUnitPosition.positionCoordinateY": "pa_y",
        "replicate": "rep_factor",
        "block": "blk",
    }

    plot_measurements_api_fields_to_local_fields = {
        "observationUnitDbId": "plot_id",
        "observationVariableDbId": "trait_id",
        "value": "trait_value",
    }

    brapi_list_page_size = 1000

    def get_plots(self, occurrence_id: str = None) -> pd.DataFrame:

        plots_data = []

        page_num = 0

        observation_units_filters = ObservationUnitQueryParams(
            studyDbId=occurrence_id, observationLevel="plot", pageSize=self.brapi_list_page_size
        )

        while len(plots_data) >= self.brapi_list_page_size or page_num == 0:

            observation_units_filters.page = page_num

            api_response = self.get(endpoint=GET_OBSERVATION_UNITS_URL, params=observation_units_filters.dict())

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

    def get_plot_measurements(self, occurrence_id: int = None) -> pd.DataFrame:

        plot_measurements_data = []

        page_num = 0

        observations_filters = ObservationUnitQueryParams(
            studyDbId=occurrence_id, observationLevel="plot", pageSize=1000
        )

        while len(plot_measurements_data) >= self.brapi_list_page_size or page_num == 0:

            observations_filters.page = page_num

            api_response = self.get(endpoint=GET_OBSERVATIONS_URL, params=observations_filters.dict())

            if not api_response.is_success:
                raise DataReaderException(api_response.error)

            brapi_response = BaseListResponse(**api_response.body)

            print(brapi_response.metadata.pagination)

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
