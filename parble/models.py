from datetime import datetime
import json
from typing import TYPE_CHECKING, Any, BinaryIO, Dict, List, Optional

from pydantic import BaseModel, PrivateAttr, confloat

import json

if TYPE_CHECKING:
    from parble.sdk import ParbleSDK


class Timings(BaseModel):
    """
    Timings information for a file
    """

    upload: datetime
    done: Optional[datetime]

    def to_json_struct(self):
        return {"upload": self.upload.strftime("%Y-%m-%d %H:%M:%S"), "done": self.done.strftime("%Y-%m-%d %H:%M:%S")}


class Classification(BaseModel):
    """
    Classification information about a single document
    """

    automated: bool
    document_type: str
    confidence: confloat(ge=0, le=100)
    start_page: int
    end_page: int


class Field(BaseModel):
    """
    A single field that's contained inside a document
    """

    page: int
    coordinates: List[int]
    text: str
    value: str
    confidence: int
    automated: bool


class Document(BaseModel):
    """
    A single classified and predicted document
    """

    automated: bool
    classification: Classification
    header_fields: Dict[str, Field] = {}
    tables: Dict[str, Any] = {}

    @property
    def type(self) -> str:
        return self.classification.document_type


class File(BaseModel):
    """
    This model represents a File datastructure from Parble API.

    A File contains a list of identified and classified documents - each one containing predictions.
    """

    id: str
    timings: Timings
    filename: str
    automated: bool
    number_of_pages: int
    documents: List[Document]

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
            self._pdf = self._sdk.files.get_pdf(self.id)
        return self._pdf

    @pdf.deleter
    def pdf(self):
        self._pdf = None

    @property
    def name(self) -> str:
        """
        Return the filename of this file
        """
        return self.filename

    def __iter__(self):
        """
        Iterating on a file will yield the documents contained in it
        """
        yield from self.documents

    def __getitem__(self, item):
        """
        Accessing indexed item returns documents of the file
        """
        return self.documents[item]

    @staticmethod
    def from_json(json_data: str):
        """
        decoding a json string to a File object
        """
        attrs = json.loads(json_data)
        attrs["sdk"] = "ParbleSDK"
        return File.parse_obj(attrs)

    def to_json(self):
        """
        Convert a File object to a json string
        """
        return json.dumps(self, default=self.__convert_to_json_struct)

    @staticmethod
    def __convert_to_json_struct(o):
        if hasattr(o, "to_json_struct") and callable(o.to_json_struct):
            return o.to_json_struct()
        return o.__dict__
