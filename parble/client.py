from parble.resources.files import FilesResource
from parble.session import BaseSession
from parble.settings import Settings


class ParbleAPIClient:
    """
    Low level REST API Client

    This thin layer exposes the API resources

    """

    def __init__(self, url=None, api_key=None):
        self.settings = Settings(url=url, api_key=api_key)
        self._client = BaseSession(self.settings)
        self.files = FilesResource(self)

    def get(self, url, **kwargs):
        """
        Send a GET request

        Args:
            url: absolute or relative resource uri
            **kwargs:

        Returns:
            API Response
        """
        return self._client.get(url, **kwargs)

    def post(self, url, **kwargs):
        """
        Send a POST request

        Args:
            url: absolute or relative resource uri
            **kwargs:

        Returns:
            API Response
        """
        return self._client.post(url, **kwargs)

    def patch(self, url, **kwargs):
        """
        Send a PATCH request

        Args:
            url: absolute or relative resource uri
            **kwargs:

        Returns:
            API Response
        """
        return self._client.patch(url, **kwargs)

    def delete(self, url, **kwargs):
        """
        Send a DELETE request

        Args:
            url: absolute or relative resource uri
            **kwargs:

        Returns:
            API Response
        """
        return self._client.delete(url, **kwargs)
