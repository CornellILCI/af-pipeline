import os

AFDB_URI = os.getenv("AFDB_URL")

UNIVERSAL_UNKNOWN = "NA"

ASREML_INPUTS_DIR = os.getenv("ASREML_INPUTS_DIR")

AF_DATA_DIR = os.getenv("AF_DATA_DIR")


def get_afdb_uri():
    return os.getenv("AFDB_URL")


def get_asreml_input_directory(request_id: str):
    """Return asreml input directory for given request id."""
    asreml_inputs_dir = os.path.join(ASREML_INPUTS_DIR, request_id)

    if os.path.exists(asreml_inputs_dir):
        return asreml_inputs_dir

    os.makedirs(asreml_inputs_dir)
    return asreml_inputs_dir


def get_analysis_engine_script(engine_name: str):
    if engine_name.lower() == "asreml":
        return "/app/scripts/asreml"
