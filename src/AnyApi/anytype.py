import requests

from .error import (
    APIError,
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ResourceDeletedError,
    UnauthorizedError,
)

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
        if not response.ok:
            map_error(response)
        return response.json()

    def post(self, path, data=None, **kwargs):
        """Send a POST request to the Anytype API using JSON payload data."""
        response = self.session.post(
            f"{self.base_url}{path}",
            json=data,
            **kwargs,
        )
        if not response.ok:
            map_error(response)
        return response.json()

    def list_spaces(self, offset: int = 0, limit: int = 100) -> AnySpacesResponse:
        """Retrieves a paginated list of all spaces that are accessible by the authenticated user.


        Args:
            offset: The number of items to skip before starting to collect the result set
            limit: The number of items to return

        Raises:
            UnauthenticatedError: Unauthorized
            InternalServerError: Internal server error

        Returns:
            The list of spaces accessible by the authenticated user
        """
        return AnySpacesResponse.model_validate(
            self.get(build_url("v1", "spaces", offset=offset, limit=limit))
        )

    def get_space(self, space_id: str) -> AnySpace:
        """Fetches full details about a single space identified by its space ID.

        Args:
            space_id: The ID of the space to retrieve; must be retrieved from ListSpaces endpoint

        Raises:
            UnauthenticatedError: Unauthorized
            NotFoundError: Not found
            InternalServerError: Internal server error

        Returns:
            The space details
        """
        return AnySpace.model_validate(
            self.get(build_url("v1", "spaces", space_id))["space"]
        )

    def list_objects(
        self, space_id: str, offset: int = 0, limit: int = 100
    ) -> AnyObjectsResponse:
        """Retrieves a paginated list of objects in the given space.

        Args:
            space_id: The ID of the space in which to list objects; must be retrieved from ListSpaces endpoint
            offset: The number of items to skip before starting to collect the result set
            limit: The number of items to return

        Raises:
            UnauthenticatedError: Unauthorized
            InternalServerError: Internal server error

        Returns:
            The list of objects in the specified space
        """
        return AnyObjectsResponse.model_validate(
            self.get(
                build_url(
                    "v1", "spaces", space_id, "objects", offset=offset, limit=limit
                )
            )
        )

    def get_object(self, space_id: str, object_id: str) -> AnyObject:
        """Fetches the full details of a single object identified by the object ID within the specified space.

        Args:
            space_id: The ID of the space in which the object exists; must be retrieved from ListSpaces endpoint
            object_id: The ID of the object to retrieve; must be retrieved from ListObjects, SearchSpace or GlobalSearch endpoints or obtained from response context

        Raises:
            UnauthenticatedError: Unauthorized
            NotFoundError: Not found
            ResourceDeletedError: Resource deleted
            InternalServerError: Internal server error

        Returns:
            The retrieved object
        """
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
        +
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


ERROR_MAP: dict[int, type[APIError]] = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    410: ResourceDeletedError,
    429: RateLimitError,
}


def map_error(response: requests.Response) -> None:
    data = response.json()
    print(response.__repr__())

    error_type = ERROR_MAP.get(response.status_code, APIError)

    raise error_type(
        message=data["error"],
        status=response.status_code,
    )
