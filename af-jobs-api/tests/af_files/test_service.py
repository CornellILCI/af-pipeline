from af_files import api_models
from af_files import service

def test_get_files_not_empty():
    
    files: list[api_models.File] = service.get_files()
    assert len(files) > 0

def test_get_files_return_files_from_directory(temp_dir):

    
