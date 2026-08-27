import requests

from AnyApi.util.url import build_url

from .model import AnySpacesResponse, AnySpace


class Anytype:
    def __init__(self, api_key, base_url="http://127.0.0.1:31009"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            "Authorization": f"Bearer {api_key}",
            "Anytype-Version": "2025-11-08",
        })

    def get(self, path, **kwargs):
        response = self.session.get(
            f"{self.base_url}{path}",
            **kwargs,
        )
        response.raise_for_status()
        return response.json()

    def spaces(self, offset:int=0, limit:int=100) -> AnySpacesResponse:
        return AnySpacesResponse.model_validate(self.get(build_url("v1", "spaces", offset=offset, limit=limit)))

    def space(self, space_id: str) -> AnySpace:
        return AnySpace.model_validate(self.get(build_url("v1", "spaces", space_id))["space"])
    
    def objects(self, space_id:str, offset:int=0, limit:int=100):
        return self.get(build_url("v1", "spaces", space_id, "objects", offset=offset, limit=limit))
