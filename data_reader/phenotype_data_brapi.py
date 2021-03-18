import pandas as pd

from models import ObservationUnitPathParams

from data_reader.phenotype_data import PhenotypeData

from exceptions import DataReaderException

GET_OBSERVATION_UNITS_URL = ("/observationunits")


class PhenotypeDataBrapi(PhenotypeData):
    """ reads phenotype data from a brapi ebs data source .
    """

    PLOTS_API_FIELDS_TO_LOCAL_FIELDS = {
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

    def get_plots(self, occurrence_id: str = None) -> pd.DataFrame:

        observation_units_filters = ObservationUnitPathParams(
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
        ).drop_duplicates()

        plots_df = plots_df_observation_levels_droped.join(
            plots_df_observation_levels_pivoted,
            on="observationUnitDbId"
        )

        # keep only local field columns
        plots_df_columns_to_drop = (
            set(plots_df.columns) -
            self.PLOTS_API_FIELDS_TO_LOCAL_FIELDS.keys())
        plots_df_columns_to_keep = (
            self.PLOTS_API_FIELDS_TO_LOCAL_FIELDS.keys() -
            plots_df_columns_to_drop)
        plots_df = plots_df[plots_df_columns_to_keep]

        # rename dataframe column with local field names
        plots_df.rename(
            columns=self.PLOTS_API_FIELDS_TO_LOCAL_FIELDS,
            inplace=True
        )

        # since plot_qc not defined in brapi spec, set default value "G"
        plots_df["plot_qc"] = "G"

        return plots_df

    def get_plot_measurements(
            self,
            occurrence_id: int = None) -> pd.DataFrame:
        raise NotImplementedError

    def get_occurrence(self, occurrence_id: int = None):
        raise NotImplementedError

    def get_experiment(self, experiment_id: int = None):
        raise NotImplementedError

    def get_trait(self, trait_id: int = None):
        raise NotImplementedError
