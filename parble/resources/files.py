import typing as t

from pydantic import constr

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
        inbox_id: constr(regex=r'^[a-f0-9]{24}$') = None,
        content_type="application/octet-stream",
    ) -> t.Dict[str, t.Any]:

        files = {
            "file": (file_name, file_content, content_type)
        }
        if inbox_id:
            files["inbox_id"] = inbox_id

        res = self._client.post(
            self.__uri__,
            files=files,
            timeout=300,
        )
        if res.ok:
            return res.json()
