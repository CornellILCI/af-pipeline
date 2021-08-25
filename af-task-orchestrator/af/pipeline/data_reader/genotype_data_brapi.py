import pandas as pd
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.data_reader.models import Occurrence
from af.pipeline.data_reader.models.brapi.core import BaseListResponse, Study
from af.pipeline.data_reader.models.brapi.phenotyping import ObservationUnitQueryParams
from af.pipeline.data_reader.phenotype_data import PhenotypeData
from af.pipeline.pandasutil import df_keep_columns
from pydantic import ValidationError

GET_OBSERVATION_UNITS_URL = "/observationunits"

GET_OBSERVATIONS_URL = "/observations"

GET_STUDIES_BY_ID_URL = "/studies/{studyDbId}"  # noqa:


class GenotypeDataBrapi(PhenotypeData):

    brapi_list_page_size = 1000

    def get_variantsets(self, occurrence_id: str = None) -> tuple:
        return "",""
