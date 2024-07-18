import requests
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.data_reader.models import ApiResponse
from af.pipeline.data_reader.urlutil import url_join, valid_url
from requests.exceptions import HTTPError, RequestException


class DataReader:
    """Reads data from HTTP web service."""

    def __init__(self, api_base_url: str = None, api_bearer_token: str = None):
        """Constructs DataReader.

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
        """Wrapper for methods in requests module.

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

        Raises:
            DataReaderException for any connection or timeout errors.
        """

        url = url_join(self.api_base_url, endpoint)
        #headers = {'Content-Type': 'application/json'}
        
        if isinstance(self.api_bearer_token, str):
            token_header = f"Bearer {self.api_bearer_token}"
            kwargs.setdefault("headers", {})["Authorization"] = token_header

        #kwargs.setdefault("headers",{})["Content-Type"]="application/json" #maybe?
        #kwargs.headers['Content-Type']='application/json'#Maybe?  
        #print(f"Api token: {token_header}")
            
        try:
            response:requests.models.Response = request_method(url, **kwargs)#Headers = headers looks stupid, but is right syntax based on stackoverflow? -JDLS
        except RequestException as r_e:
            raise DataReaderException(r_e)

        if (response.status_code == 400):print(f"Code: {response.status_code} Body: {response.content}")
        try:
            api_response = ApiResponse(http_status=response.status_code, body=response.json())
        except requests.exceptions.JSONDecodeError:
            print(f"BrAPI response was not real JSON {response.status_code}  ||  {response.content}")
            api_response = ApiResponse(http_status=response.status_code,body=response.content)#Body was not valid json - seems to happen in POSTs to Gigwa... probably GIGWA correct, and naive assumption that everything is valid .json is wrong - JDLS

        try:
            response.raise_for_status()
            api_response.is_success = True
        except HTTPError as h_e:
            api_response.error = repr(h_e)

        return api_response

    def get(self, endpoint: str = None, **kwargs) -> ApiResponse:
        """Subimits http GET requsts from the given endpoint.

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

        Raises:
            DataReaderException for any connection or timeout errors.
        """
        return self._request(requests.get, endpoint, **kwargs)

    def post(self, endpoint: str = None, **kwargs) -> ApiResponse:
        """Subimits http POST requsts from the given endpoint.

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

        Raises:
            DataReaderException for any connection or timeout errors.
        """
        return self._request(requests.post, endpoint, **kwargs)
