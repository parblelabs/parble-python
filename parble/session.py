from urllib.parse import urljoin

from requests import HTTPError, PreparedRequest, Request, RequestException, Response, Session
from requests import Timeout as RequestTimeout

from parble._version import __version__
from parble.exceptions import APICallError, CallTimeoutError, handlers
from parble.settings import Settings


class BaseSession(Session):
    """
    Base requests session with shared behavior for the API Calls.

    Provides base url support, custom headers and common error handling.
    """

    def __init__(self, settings: Settings):
        super().__init__()
        self._settings = settings
        self.initialize()

    def initialize(self):
        """
        Initialize the session by setting the headers to use
        """
        self.headers["X-API-Key"] = self._settings.api_key.get_secret_value()
        self.headers["Accept"] = "application/json"
        self.headers["User-Agent"] = f"parble-python/{__version__}"

    def build_url(self, url: str) -> str:
        """
        Join the base URL with the provided URI

        Args:
            url: resource part to add to the base url

        Returns:
            Full concatenated URL
        """
        return urljoin(str(self._settings.url), url)

    def request(self, method: str, url: str, *args, **kwargs) -> Response:
        kwargs.setdefault("timeout", self._settings.default_timeout)
        try:
            resp = super().request(method, url, *args, **kwargs)
            resp.raise_for_status()
            return resp
        except RequestTimeout as exc:
            raise CallTimeoutError from exc
        except HTTPError as exc:
            self.parse_error(exc)
        except RequestException as exc:
            raise APICallError from exc

    def prepare_request(self, request: Request) -> PreparedRequest:
        request.url = self.build_url(request.url)
        return super().prepare_request(request)

    def parse_error(self, err: HTTPError):
        code = err.response.status_code
        exc = handlers.get(code, APICallError)
        raise exc(*err.args) from err
