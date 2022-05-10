from dataclasses import dataclass, field

from af.pipeline.data_reader.models import Occurrence  # noqa: E402; noqa: E402


@dataclass
class JobParams:

    formula: str = None
    residual: str = None
    predictions: list[str] = None
    analysis_fields_types: dict = None  # field datatypes.


@dataclass
class JobData:
    """Class for keeping data to run successful job like data file path and other related meta data for engines."""

    job_name: str = ""

    job_result_dir: str = ""
    data_file: str = ""

    job_file: str = ""
    job_params: JobParams = None

    metadata_file: str = ""

    occurrences: list[Occurrence] = field(default_factory=list)
    trait_name: str = ""
    location_name: str = ""
