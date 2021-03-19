import pandas as pd

from pydantic import ValidationError

from models import ObservationUnitQueryParams, Study, Occurrence

from data_reader.phenotype_data import PhenotypeData

from exceptions import DataReaderException

GET_OBSERVATION_UNITS_URL = ("/observationunits")

GET_OBSERVATIONS_URL = ("/observations")

GET_STUDIES_BY_ID_URL = ("/studies/{studyDbId}")


class PhenotypeDataBrapi(PhenotypeData):
    """ reads phenotype data from a brapi ebs data source .
    """

    plots_api_fields_to_local_fields = {
        "observationUnitDbId": "plot_id",
        "germplasmDbId": "entry_id",
        "studyDbId": "occurrence_id",
        "trialDbId": "experiment_id",
        "locationDbId": "location_id",
        "observationUnitPosition.positionCoordinateX": "pa_x",
        "observationUnitPosition.positionCoordinateY": "pa_y",
        "replicate": "rep_factor",
        "block": "blk"
    }

    plot_measurements_api_fields_to_local_fields = {
        "observationUnitDbId": "plot_id",
        "observationVariableDbId": "trait_id",
        "value": "trait_value"
    }

    def get_plots(self, occurrence_id: str = None) -> pd.DataFrame:

        observation_units_filters = ObservationUnitQueryParams(
            studyDbId=occurrence_id,
            observationLevel="plot",
            pageSize=1000
        )

        api_response = self.get(endpoint=GET_OBSERVATION_UNITS_URL,
                                params=observation_units_filters.dict())

        if not api_response.is_success:
            raise DataReaderException(api_response.error)

        plots_data = api_response.body["result"]["data"]

        # paths to normalize json data to flat columns
        columns_path = [
            "observationUnitDbId",
            "locationDbId",
            "studyDbId",
            "trialDbId",
            "germplasmDbId",
            ["observationUnitPosition", "positionCoordinateX"],
            ["observationUnitPosition", "positionCoordinateY"]
        ]

        # list record path to normalze
        list_record_path = ["observationUnitPosition",
                            "observationLevelRelationships"]

        # this dataframe will have observation level array as seperate rows
        plots_df_unpivoted = pd.json_normalize(
            plots_data,
            record_path=list_record_path,
            meta=columns_path,
        )

        plots_df_observation_levels_pivoted = plots_df_unpivoted.pivot(
            index="observationUnitDbId",
            columns="levelName",
            values="levelCode")

        plots_df_observation_levels_droped = plots_df_unpivoted.drop(
            columns=["levelOrder", "levelCode", "levelName"]
        ).drop_duplicates().reset_index()

        plots_df = plots_df_observation_levels_droped.join(
            plots_df_observation_levels_pivoted,
            on="observationUnitDbId"
        )

        # keep only local field columns
        plots_df_columns_to_drop = (
            set(plots_df.columns) -
            self.plots_api_fields_to_local_fields.keys())
        plots_df_columns_to_keep = (
            self.plots_api_fields_to_local_fields.keys() -
            plots_df_columns_to_drop)
        plots_df = plots_df[plots_df_columns_to_keep]

        # rename dataframe column with local field names
        plots_df.rename(
            columns=self.plots_api_fields_to_local_fields,
            inplace=True
        )

        # since plot_qc not defined in brapi spec, set default value "G"
        plots_df["plot_qc"] = "G"

        return plots_df.astype(str)

    def get_plot_measurements(
            self,
            occurrence_id: int = None) -> pd.DataFrame:

        observation_units_filters = ObservationUnitQueryParams(
            studyDbId=occurrence_id,
            observationLevel="plot",
            pageSize=1000
        )

        api_response = self.get(endpoint=GET_OBSERVATIONS_URL,
                                params=observation_units_filters.dict())

        if not api_response.is_success:
            raise DataReaderException(api_response.error)

        api_result = api_response.body["result"]

        plot_measurements = pd.DataFrame(api_result["data"])

        # keep only local field columns
        plot_measurements_columns_to_drop = (
            set(plot_measurements.columns) -
            self.plot_measurements_api_fields_to_local_fields.keys())
        plot_measurements_columns_to_keep = (
            self.plot_measurements_api_fields_to_local_fields.keys() -
            plot_measurements_columns_to_drop)
        plot_measurements = plot_measurements[
            plot_measurements_columns_to_keep]

        # rename dataframe column with local field names
        plot_measurements.rename(
            columns=self.plot_measurements_api_fields_to_local_fields,
            inplace=True
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
            location=_study.locationName
        )

    def get_experiment(self, experiment_id: int = None):
        raise NotImplementedError

    def get_trait(self, trait_id: int = None):
        raise NotImplementedError
