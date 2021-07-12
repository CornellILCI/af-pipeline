import hashlib
import re
import os

from pathlib import Path

import zipfile


def get_analysis_engine(analysis_request):
    engine = analysis_request["metadata"]["engine"]
    engine = re.sub("-.*", "", engine)
    engine = engine.lower()
    return engine


def get_request_type(analysis_request):
    request_id = analysis_request["metadata"]["id"]
    req_type = re.sub("_0000", "", request_id)
    req_type = re.sub(r".+?\_", "", req_type)
    return req_type


def get_request_sha(analysis_request):
    request_id = analysis_request["metadata"]["id"]
    hash_ = hashlib.sha1(request_id.encode("utf-8"))
    return hash_.hexdigest()


def get_job_status(stdout, stderr):
    # TODO: Check for better way to represent job status
    err_found = len(stderr) > 0
    out_found = len(stdout) > 0
    if err_found and out_found:
        return 111
    elif err_found and not out_found:
        return 101
    elif not err_found and out_found:
        return 110
    elif not (err_found and out_found):
        return 100


def get_parent_dir(file_path: str) -> str:
    _file_path = Path(file_path)
    return _file_path.parent


def zip_dir(dir_to_zip: str, output_file_path: str, base_dir: str):
    """Zips the input directory to destination zip file"""

    files_to_zip = []

    for root, directories, files in os.walk(dir_to_zip):

        for file_name in files:

            file_path = os.path.join(root, file_name)
            files_to_zip.append(file_path)

    _zip_file = zipfile.ZipFile(output_file_path, "a")

    with _zip_file:
        for _file in files_to_zip:
            _dest_name = f"{base_dir}/{os.path.basename(_file)}"
            _zip_file.write(_file, _dest_name, zipfile.ZIP_DEFLATED)
