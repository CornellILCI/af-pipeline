import os


def get_allowable_origins():
    allowable_origins = os.getenv("AFAPI_ALLOWABLE_ORIGINS")
    if allowable_origins is not None:
        allowable_origins = allowable_origins.split(";")
    return allowable_origins
