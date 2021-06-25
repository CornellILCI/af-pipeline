import os

AFDB_URI = os.getenv("AFDB_URL")

UNIVERSAL_UNKNOWN = "NA"


def get_analysis_engine_script(engine_name: str):

    if engine_name.lower() == "asreml":
        return "/app/scripts/asreml"
