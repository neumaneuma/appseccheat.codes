import os
from collections.abc import Mapping
from urllib.request import url2pathname

from requests import Response
from requests.adapters import HTTPAdapter
from requests.models import PreparedRequest


class LocalFileAdapter(HTTPAdapter):
    """Protocol Adapter to allow Requests to GET file:// URLs"""

    @staticmethod
    def _chkpath(path: str) -> tuple[int, str]:
        """Return an HTTP status for the given filesystem path."""
        if os.path.isdir(path):
            return 400, "Path Not A File"
        elif not os.path.isfile(path):
            return 404, "File Not Found"
        elif not os.access(path, os.R_OK):
            return 403, "Access Denied"
        else:
            return 200, "OK"

    def send(
        self,
        request: PreparedRequest,
        stream: bool = False,
        timeout: float | tuple[float, float] | tuple[float, None] | None = None,
        verify: bool | str = True,
        cert: bytes | str | tuple[bytes | str, bytes | str] | None = None,
        proxies: Mapping[str, str] | None = None,
    ) -> Response:
        """Return the file specified by the given request"""
        path = os.path.normcase(os.path.normpath(url2pathname(request.path_url)))
        response = Response()

        response.status_code, response.reason = self._chkpath(path)
        if response.status_code == 200:
            try:
                response.raw = open(path, "rb")
            except OSError as err:
                response.status_code = 500
                response.reason = str(err)

        if request.url is None:
            raise ValueError("Request URL is None")
        response.url = request.url
        response.request = request
        response.connection = self

        return response

    def close(self) -> None:
        pass
