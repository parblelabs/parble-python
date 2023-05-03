import typing as t
from io import BytesIO
from mimetypes import guess_type
from pathlib import Path

from .client import ParbleAPIClient
from .models import File


class ParbleSDK:
    """
    High Level SDK Class

    This class exposes primitives built on top of the :py:class:`ParbleAPIClient`

    """

    def __init__(self, url=None, api_key=None):
        self.client = ParbleAPIClient(url=url, api_key=api_key)
        self.files = self.Files(self.client)

    class Files:
        def __init__(self, client: ParbleAPIClient):
            self.client = client

        def post(self, path: t.Union[str, Path]) -> File:
            """
            Upload and process the file at the given local path

            Args:
                path: local path of the file to upload

            Returns:
                Processed File response
            """
            if not isinstance(path, Path):
                path = Path(path)

            file_name = path.name
            file_type, encoding = guess_type(path)
            if not file_type:
                file_type = "application/octet-stream"
            with open(path.absolute(), "rb") as f:
                res = self.client.post(f, file_name, content_type=file_type)
            return self.create(**res)

        def post_file(self, file: t.BinaryIO, file_name: str, file_type="application/octet-stream") -> File:
            """
            Upload and process the given file-like

            This function requires you to specify the filename which will be sent. You can also specify
            the file type as a hint to help inferring the proper payload content type; else this will be treated
            as an octet stream.

            Args:
                file: File-like object
                file_name: Filename to be used
                file_type: Content Type of the file

            Returns:
                Processed File data
            """
            res = self.client.post(file, file_name, content_type=file_type)
            return self.create(**res)

        def get(self, file_id: str) -> File:
            """
            Retrieve the given File payload

            Args:
                file_id: File ID to get

            Returns:
                Matching File
            """
            res = self.client.get(file_id)
            return self.create(**res)

        def get_pdf(self, file_id: str) -> t.BinaryIO:
            """
            Retrieve the given File PDF content

            Args:
                file_id: File ID to get

            Returns:
                File-like PDF content
            """
            res = self.client.get(file_id, content_type="application/pdf")
            return BytesIO(res)

        def create(self, **attrs: t.Any) -> File:
            """
            Create a File object from a dict of attributes

            On top of the attributes from the API, Files require to be bound to an active SDK instance,
            which this helper function makes sure.

            Args:
                attrs: Attributes payload from the API Call

            Returns:
                parsed File object
            """
            attrs["sdk"] = self
            return File.parse_obj(attrs)
