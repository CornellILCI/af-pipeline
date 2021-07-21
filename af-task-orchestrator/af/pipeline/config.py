import os

AFDB_URI = os.getenv("AFDB_URL")

UNIVERSAL_UNKNOWN = "NA"


def get_afdb_uri():
    return os.getenv("AFDB_URL")


def get_analysis_engine_script(engine_name: str):
    # This needs to configured from db
    if engine_name.lower() == "asreml":
        return "asreml"
