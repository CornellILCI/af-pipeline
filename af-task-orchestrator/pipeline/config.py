import os

AFDB_URI = os.getenv("AFDB_URL")

UNIVERSAL_UNKNOWN = "NA"


# for better dependency injection
def get_afdb_uri():
    return os.getenv("AFDB_URL")
