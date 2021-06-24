from functools import wraps
from flask import request, jsonify

from pydantic import ValidationError
from common import api_models

from http import HTTPStatus

def validate_api_request(query_model=None, body_model=None):
    """Validate api requests query and body parameters for given
    pydantic models.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            if body_model:
                try:
                    body_model(**request.json)
                except ValidationError as e:
                    error_response = api_models.ErrorResponse(errorMsg=str(e))
                    return jsonify(error_response.dict()), HTTPStatus.BAD_REQUEST

            if query_model:
                try:
                    query_model(**request.args)
                except ValidationError as e:
                    error_response = api_models.ErrorResponse(errorMsg=str(e))
                    return jsonify(error_response.dict()), HTTPStatus.BAD_REQUEST

            return func(*args, **kwargs)

        return wrapper
    return decorator
