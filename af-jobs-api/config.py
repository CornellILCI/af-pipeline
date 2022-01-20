import os

ROOT_DATA_FOLDER = os.getenv("BA_DATA_DIR")

ANALYSIS_RESULT_FILE_NAME = "result.zip"

RESULT_DOWNLOAD_BY_REQUEST = "/requests/{request_id}/files/{file_name}"


def get_analysis_request_folder(request_id: str) -> str:
    """Returns the shared data folder path for given request id."""
    return os.path.join(ROOT_DATA_FOLDER, "analysis", request_id)


def get_analysis_result_file_path(request_id: str) -> str:

    request_folder = get_analysis_request_folder(request_id)

    return os.path.join(request_folder, ANALYSIS_RESULT_FILE_NAME)


def get_allowable_origins():
    allowable_origins = os.getenv("AFAPI_ALLOWABLE_ORIGINS")
    if allowable_origins is not None:
        allowable_origins = allowable_origins.split(";")
    return allowable_origins


def get_result_download_url(request_id: str):

    return RESULT_DOWNLOAD_BY_REQUEST.format(request_id=request_id, file_name=ANALYSIS_RESULT_FILE_NAME)
