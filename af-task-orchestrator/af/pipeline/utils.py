import hashlib
import re


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
