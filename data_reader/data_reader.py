import requests

from common import valid_url, url_join

from models import ApiResponse

from exceptions import DataReaderException


class DataReader:
    def __init__(self,
                 api_base_url: str = None,
                 api_bearer_token: str = None):

        if not valid_url(api_base_url):
            raise DataReaderException(f"Invalid api base url: {api_base_url}")

        self.api_base_url = api_base_url
        self.api_bearer_token = api_bearer_token

    def _request(self, request_method, endpoint, **kwargs):
        url = url_join(self.api_base_url, endpoint)

        if isinstance(self.api_bearer_token, str):
            token_header = f"Bearer {self.api_bearer_token}"
            kwargs.setdefault("headers", {})["Authorization"] = token_header

        response = request_method(url, **kwargs)

        if response.status_code == 200:
            return ApiResponse(body=response.json(),
                               is_success=True,
                               error=None)
        else:
            return ApiResponse(body=None,
                               is_success=False,
                               error=response.json())

    def get(self, endpoint: str = None, **kwargs) -> ApiResponse:
        """ subimits http GET requsts from the given endpoint
        params:
            endpoint: relative endpoint to base url
            kwargs: valid requests arguments like below
                {
                    params: dictionary object with query parameters if any
                    headers: dictionary object for headers
                    body: body of the post request
                }
        """
        return self._request(requests.get, endpoint, **kwargs)

    def post(self, endpoint: str = None, **kwargs) -> ApiResponse:
        """ subimits http POST requsts from the given endpoint
        params:
            endpoint: relative endpoint to base url
            kwargs: valid requests arguments like below
                {
                    params: dictionary object with query parameters if any
                    headers: dictionary object for headers
                    body: body of the post request
                }
        """
        return self._request(requests.post, endpoint, **kwargs)
