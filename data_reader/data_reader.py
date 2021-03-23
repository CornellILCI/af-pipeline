import requests

from common import valid_url, url_join

from models import ApiResponse

from exceptions import DataReaderException


class DataReader:
    """ Reads data from HTTP web service.
    """

    def __init__(self,
                 api_base_url: str = None,
                 api_bearer_token: str = None):
        """ Constructs DataReader.

        Args:
            api_base_url:
                Base url of the API to which endpoints are relative to.
                eg: https://api.gobii.org/gdm/crops/dev/brapi/v2
            api_bearer_token:
                API access token. Passed as http header for
                Bearer Authorization
        """

        if not valid_url(api_base_url):
            raise DataReaderException(f"Invalid api base url: {api_base_url}")

        self.api_base_url = api_base_url
        self.api_bearer_token = api_bearer_token

    def _request(self, request_method, endpoint, **kwargs):
        """ Wrapper for methods in requests module.

        Args:
            request_method:
                Request method to apply, requests.get or requests.post.
            endpoint:
                Relative endpoint to the base url to which request method
                needs to be applied.
            kawrgs:
                Request paramteres, like body, query params and headers.
        Returns:
            ApiResponse object with the body of response.

            If failed, returns ApiResponse object with error response
            as value for error field.
        """

        url = url_join(self.api_base_url, endpoint)

        if isinstance(self.api_bearer_token, str):
            token_header = f"Bearer {self.api_bearer_token}"
            kwargs.setdefault("headers", {})["Authorization"] = token_header

        response = request_method(url, **kwargs)

        if response.status_code == 200:
            return ApiResponse(body=response.json(),
                               is_success=True)
        else:
            return ApiResponse(is_success=False,
                               error=response.json())

    def get(self, endpoint: str = None, **kwargs) -> ApiResponse:
        """ Subimits http GET requsts from the given endpoint.

        Args:
            endpoint:
                Relative endpoint to base url.
            kwargs:
                Valid requests arguments like below
                {
                    params: dictionary object with query parameters if any
                    headers: dictionary object for headers
                    body: body of the post request
                }

        Returns:
            ApiResponse object with the body of response.

            If failed, returns ApiResponse object with error response
            as value for error field.
        """
        return self._request(requests.get, endpoint, **kwargs)

    def post(self, endpoint: str = None, **kwargs) -> ApiResponse:
        """ Subimits http POST requsts from the given endpoint.

        Args:
            endpoint: relative endpoint to base url
            kwargs: valid requests arguments like below
                {
                    params: dictionary object with query parameters if any
                    headers: dictionary object for headers
                    body: body of the post request
                }

        Returns:
            ApiResponse object with the body of response.

            If failed, returns ApiResponse object with error response
            as value for error field.
        """
        return self._request(requests.post, endpoint, **kwargs)
