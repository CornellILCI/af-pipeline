import os

ROOT_DATA_FOLDER = os.getenv("AF_DATA_DIR")


def get_analysis_request_folder(request_id: str) -> str:
    """Returns the shared data folder path for given request id."""

    if ROOT_DATA_FOLDER is None:
        return None
    return os.path.join(ROOT_DATA_FOLDER, "analysis", request_id)


def get_allowable_origins():
    allowable_origins = os.getenv("AFAPI_ALLOWABLE_ORIGINS")
    if allowable_origins is not None:
        allowable_origins = allowable_origins.split(";")
    return allowable_origins
