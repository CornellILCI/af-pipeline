import pandas as pd
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.data_reader.models import Occurrence
from af.pipeline.data_reader.models.brapi.core import BaseListResponse, Study
from af.pipeline.data_reader.models.brapi.phenotyping import ObservationUnitQueryParams
from af.pipeline.data_reader.phenotype_data import PhenotypeData
from af.pipeline.pandasutil import df_keep_columns
from pydantic import ValidationError

GET_OBSERVATION_UNITS_URL = "/variantsets"


class GenotypeDataBrapi(PhenotypeData):

    brapi_list_page_size = 1000

    def get_variantsets(self, studyDbIds: list[str] = None) -> tuple:

        observation_units_filters = VariantSetRequest(
            callSetDbIds=occurrence_id
            
        )


        return "",""
