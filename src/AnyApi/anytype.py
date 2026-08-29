import requests

from .util.url import build_url

from .model import AnySpacesResponse, AnySpace, AnyObject, AnyObjectsResponse


class Anytype:
    """Client for interacting with the Anytype API."""

    def __init__(self, api_key, base_url="http://127.0.0.1:31009"):
        """Create a configured API client for a local or remote Anytype instance.

        Args:
            api_key: Bearer token used to authenticate requests.
            base_url: Base URL of the Anytype server. Defaults to the local API.
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}",
                "Anytype-Version": "2025-11-08",
            }
        )

    def get(self, path, **kwargs):
        """Send a GET request to the Anytype API and return the JSON payload."""
        response = self.session.get(
            f"{self.base_url}{path}",
            **kwargs,
        )
        response.raise_for_status()
        return response.json()

    def post(self, path, data=None, **kwargs):
        """Send a POST request to the Anytype API using JSON payload data."""
        response = self.session.post(
            f"{self.base_url}{path}",
            json=data,
            **kwargs,
        )
        response.raise_for_status()
        return response.json()

    def spaces(self, offset: int = 0, limit: int = 100) -> AnySpacesResponse:
        """Fetch a paginated list of spaces from the API.

        Args:
            offset: Number of items to skip.
            limit: Maximum number of items to return.
        """
        return AnySpacesResponse.model_validate(
            self.get(build_url("v1", "spaces", offset=offset, limit=limit))
        )

    def space(self, space_id: str) -> AnySpace:
        """Fetch the details for a single space by its identifier."""
        return AnySpace.model_validate(
            self.get(build_url("v1", "spaces", space_id))["space"]
        )

    def objects(
        self, space_id: str, offset: int = 0, limit: int = 100
    ) -> AnyObjectsResponse:
        """List objects belonging to a specific space."""
        return AnyObjectsResponse.model_validate(
            self.get(
                build_url(
                    "v1", "spaces", space_id, "objects", offset=offset, limit=limit
                )
            )
        )

    def object(self, space_id: str, object_id: str) -> AnyObject:
        """Fetch one object from a space by its object identifier."""
        return AnyObject.model_validate(
            self.get(build_url("v1", "spaces", space_id, "objects", object_id))[
                "object"
            ]
        )

    def object_by_types(
        self,
        type_keys: list[str],
        space_id: str | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> AnyObjectsResponse:
        """Search for objects by one or more type keys.

        Args:
            type_keys: Type keys to match.
            space_id: Optional space to scope the search to.
            offset: Number of items to skip.
            limit: Maximum number of items to return.
        """
        return AnyObjectsResponse.model_validate(
            self.post(
                (
                    build_url("v1", "search", offset=offset, limit=limit)
                    if space_id is None
                    else build_url("v1", "spaces", space_id, "search")
                ),
                data={"types": type_keys},
            )
        )
