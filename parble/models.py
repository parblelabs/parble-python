from typing import TYPE_CHECKING, Any, BinaryIO, Optional

from pydantic import BaseModel, PrivateAttr

if TYPE_CHECKING:
    from parble.sdk import ParbleSDK


class File(BaseModel):
    """
    This model represents a File datastructure from Parble API.
    """

    id: str

    _sdk: Optional["ParbleSDK"] = PrivateAttr()
    _pdf: Optional[BinaryIO] = PrivateAttr(default=None)

    def __init__(self, sdk: "ParbleSDK", **data: Any):
        super().__init__(**data)
        self._sdk = sdk

    @property
    def pdf(self) -> BinaryIO:
        """
        Fetch and return the PDF representation of the processed File.

        The content is fetched from the API and cached.
        Explicitly calling del on this property will clear the cache
        """
        if self._pdf is None:
            self._pdf = self._sdk.get_file_pdf(self.id)
        return self._pdf

    @pdf.deleter
    def pdf(self):
        self._pdf = None
