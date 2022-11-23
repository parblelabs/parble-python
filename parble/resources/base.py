import abc
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from parble.client import ParbleAPIClient


class BaseResource(abc.ABC):
    __uri__: ClassVar[str]  # base uri of this resource

    def __init__(self, client):
        self._client: "ParbleAPIClient" = client
