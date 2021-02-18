# For common utils methos across packages

from urllib.parse import urljoin


def url_join(base_url: str, relative_url: str) -> str:
    base_url = base_url.rstrip("/") + "/"
    relative_url = relative_url.lstrip("/")

    return urljoin(base_url, relative_url)
