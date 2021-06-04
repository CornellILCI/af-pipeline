import os

# TODO: come up with a way to have multiple data sources
# for each EBS or BRAPI

EBS_BASE_URL = os.getenv("B4R_API_BASE_URL")

BRAPI_BASE_URL = os.getenv("BRAPI_BASE_URL")

AFDB_URL = os.getenv("AFDB_URL")

ROOT_DATA_FOLDER = os.getenv("ROOT_DATA_FOLDER")

def get_analysis_request_folder(request_id: str) -> str:
    """ Returns the shared data folder path for given request id.
    """
    analysis_request_folder = os.path.join(ROOT_DATA_FOLDER, request_id)

    if os.path.exist(analysis_request_folder):
        return analysis_request_folder

    os.mkdir(analysis_request_folder)
    return analysis_request_folder
