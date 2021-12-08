from af_files import api_models
from af_files import service

def test_get_files_match_length(job_dir, job_files):

    files: list[api_models.File] = service.get_files_by_job_name(job_name)
    assert len(files) == len(job_files)


def test_get_files_name_mapped(job_name, job_files):

    

