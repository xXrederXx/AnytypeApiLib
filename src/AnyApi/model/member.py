from typing import Literal

from pydantic import Field

from .icon import AnyIcon
from .base import APIResponseModel

MemberRole = Literal[
    "viewer",
    "editor",
    "admin",
    "owner",
    "no_permission",
]

MemberStatus = Literal[
    "joining",
    "active",
    "removed",
    "declined",
    "removing",
    "canceled",
]


class AnyMember(APIResponseModel):
    """Definition of a member in the network."""

    global_name: str = Field(
        description="The global name of the member in the network.",
    )
    icon: AnyIcon | None = Field(
        description="Icon metadata associated with the member.",
    )
    id: str = Field(
        description="The profile object id of the member.",
    )
    identity: str = Field(
        description="The identity of the member in the network.",
    )
    name: str = Field(
        description="The name of the member.",
    )
    object: str = Field(
        description="The data model of the object.",
    )
    role: MemberRole = Field(
        description="The role of the member.",
    )
    status: MemberStatus = Field(
        description="The status of the member.",
    )
