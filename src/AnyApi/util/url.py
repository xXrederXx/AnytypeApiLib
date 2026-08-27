from urllib.parse import quote, urlencode


def build_url(*parts: str, **params) -> str:
    """Build a URL from path components and query parameters.

    Each path component is percent-encoded to safely handle special characters,
    while query parameters are encoded using urllib.parse.urlencode.

    Args:
    *parts: Path components to join with /.
    **params: Query parameters to encode and append to the URL.

    Returns:
    A URL path with an encoded query string, if parameters are provided.
    """
    url = "/" + "/".join(quote(part, safe="") for part in parts)
    query = urlencode(params)
    return f"{url}?{query}" if query else url
