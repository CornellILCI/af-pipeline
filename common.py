# For common utils methods across packages

from urllib.parse import urljoin, urlparse


def valid_url(url):
    """ retruns True if url is a valid http url"""

    valid_schemes = {"http", "https"}

    if not isinstance(url, str) or not url.strip():
        return False
    urlparts = urlparse(url)

    return urlparts.scheme in valid_schemes


def url_join(base_url: str, relative_url: str) -> str:
    base_url = base_url.rstrip("/") + "/"
    relative_url = relative_url.lstrip("/")

    return urljoin(base_url, relative_url)
