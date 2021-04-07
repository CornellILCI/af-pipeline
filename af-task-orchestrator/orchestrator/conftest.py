import sys
import os

import json

os.environ["B4R_API_BASE_URL"] = ""


def read_mock_json_file(file_path):
    mock_response_file_path = os.path.join(sys.path[0], file_path)
    with open(mock_response_file_path) as mock_response_file:
        test_response = json.load(mock_response_file)
    return test_response
