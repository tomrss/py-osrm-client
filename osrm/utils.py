from enum import Enum
from typing import List, Union

from urllib.parse import quote_plus

from .model import Point


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
    url_base = f'/{service}/{api_version}/{profile}/{coord_str}'
    url_params = '&'.join(
        f'{key}={_query_param(value)}'
        for key, value in kwargs.items()
        if value is not None
    )

    return f'{url_base}?{url_params}'
