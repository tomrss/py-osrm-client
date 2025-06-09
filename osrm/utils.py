from enum import Enum
from typing import List, Union

from urllib.parse import quote_plus

from .model import Point


# TODO move this from module!
class OsrmException(Exception):
    """Exception for error response from OSRM api."""


def _build_osrm_url(
        service: str,
        api_version: str,
        profile: str,
        coordinates: List[Point],
        **kwargs,
) -> str:
    """Build url for invoking OSRM service."""

    def _query_param(value: Union[str, bool, Enum, int, float]) -> str:
        if isinstance(value, str):
            return quote_plus(value)
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, Enum):
            return value.value
        else:
            return str(value)

    coord_str = ';'.join([f'{c[0]},{c[1]}' for c in coordinates])
    url_base = f'{service}/{api_version}/{profile}/{coord_str}'
    url_params = '&'.join(
        f'{key}={_query_param(value)}'
        for key, value in kwargs.items()
        if value is not None and value != []
    )

    return f'{url_base}?{url_params}'


def _check_response(status_code: int, body: dict) -> None:
    """Check the response raising exception if error."""
    if 200 <= status_code < 300:
        return
    if 300 <= status_code < 400:
        raise OsrmException(f'unexpected redirect status code {status_code}')
    if 400 <= status_code < 500:
        if body:
            code = body.get('code', None)
            msg = body.get('message', None)
            raise OsrmException(f'bad request: {code}: {msg}')
        else:
            raise OsrmException('bad request: status code {status}')
    if 500 <= status_code < 600:
        raise OsrmException(f'internal server error {status_code}: {body}')

    raise OsrmException(f'unknown response status code {status_code}')
