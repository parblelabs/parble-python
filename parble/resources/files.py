import typing as t

from .base import BaseResource


class FilesResource(BaseResource):
    __uri__ = "files"

    def delete(self, pk: str):
        uri = f"{self.__uri__}/{pk}"
        res = self._client.delete(uri)
        if res.ok:
            return None

    def get(self, pk: str, content_type="application/json") -> t.Union[t.Dict[str, t.Any], bytes]:
        uri = f"{self.__uri__}/{pk}"
        res = self._client.get(uri, headers={"Accept": content_type})
        if res.ok:
            ct = res.headers.get("Content-Type", "application/json")
            if ct == "application/json":
                return res.json()
            return res.content

    def post(
        self,
        file_content: t.BinaryIO,
        file_name: str,
        content_type="application/octet-stream",
    ) -> t.Dict[str, t.Any]:
        res = self._client.post(
            self.__uri__,
            files={"file": (file_name, file_content, content_type)},
            timeout=300,
        )
        if res.ok:
            return res.json()
