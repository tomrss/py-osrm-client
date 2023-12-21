from typing import List, Optional

import aiohttp

from . import model
from .utils import _build_osrm_url


class OsrmAsyncClient():
    """Async Client for OSRM API.

    See https://project-osrm.org/
    See http://project-osrm.org/docs/v5.5.1/api/ for docs.
    """

    def __init__(
            self,
            base_url: str = 'http://router.project-osrm.org',
            api_version: str = 'v1',
            default_profile: str = 'driving',
    ) -> None:
        """Construct instance of OSRM client.

        :keyword str base_url: Base url of the OSRM server.
        :keyword str api_version: Api version of OSRM server.
        :keyword str default_profile: Default profile to use.
        """
        self.base_url = base_url
        self.api_version = api_version
        self.default_profile = default_profile

    async def __aenter__(self):
        """Initialize client opening the underlying http session."""
        session = aiohttp.ClientSession(base_url=self.base_url)
        self._session = await session.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        """Finalize the client closing the underlying http session."""
        await self._session.__aexit__(*args, **kwargs)

    async def nearest(
            self,
            coordinates: List[model.Point],
            profile: str = None,
            number: int = 1,
    ) -> model.OsrmNearest:
        """OSRM Nearest service.

        Snaps a coordinate to the street network and returns the
        nearest n matches.

        See http://project-osrm.org/docs/v5.5.1/api/#nearest-service

        :param coordinates: List of coordinates.
        :keyword profile: OSRM Profile, defaults to client default.
        :keyword number: Number of nearest segments that should be returned.

        :return: Nearest n matches calculated by OSRM.
        :rtype: ~model.OsrmNearest
        """
        osrm_res = await self._osrm_service(
            'nearest', profile, coordinates,
            number=number,
        )
        return model.OsrmNearest(**osrm_res)

    async def route(
            self,
            coordinates: List[model.Point],
            profile: Optional[str] = None,
            alternatives: bool = False,
            steps: bool = False,
            annotations: bool = False,
            geometries: str = 'polyline',
            overview: str = 'simplified',
            continue_straight: str = 'default',
    ) -> model.OsrmRoute:
        """OSRM Route service.

        Finds the fastest route between coordinates in the supplied order.

        See http://project-osrm.org/docs/v5.5.1/api/#route-service

        :param coordinates: List of coordinates.
        :keyword profile: OSRM Profile, defaults to client default.
        :keyword alternatives: Search for alternative routes.
        :keyword steps: Return route steps for each route leg.
        :keyword annotations: Returns additional metadata for each coordinate.
        :keyword geometries: Returned route geometry format.
        :keyword overview: Add overview geometry.
        :keyword continue_straight: Forces the route to keep going straight.

        :return: Route computed by OSRM.
        :rtype: ~model.OsrmRoute
        """
        osrm_res = await self._osrm_service(
            'route', profile, coordinates,
            alternatives=alternatives,
            steps=steps,
            geometries=geometries,
            overview=overview,
            annotations=annotations,
            continue_straight=continue_straight,
        )
        return model.OsrmRoute(**osrm_res)

    async def table(
            self,
            coordinates: List[model.Point],
            profile: Optional[str] = None,
            sources: List[int] = [],
            destinations: List[int] = [],
    ) -> model.OsrmTable:
        """OSRM Table service.

        Computes the duration of the fastest route between all pairs
        of supplied coordinates.

        See http://project-osrm.org/docs/v5.5.1/api/#table-service

        :param coordinates: List of coordinates.
        :keyword profile: OSRM Profile, defaults to client default.
        :keyword sources: Use location with given index as source.
        :keyword destinations: Use location with given index as destination.

        :return: Distance table computed by OSRM.
        :rtype: ~model.OsrmTable
        """
        sources_str = ";".join(sources) if sources else "all"
        destinations_str = ";".join(destinations) if destinations else "all"

        osrm_res = await self._osrm_service(
            'table', profile, coordinates,
            sources=sources_str,
            destinations=destinations_str,
        )
        return model.OsrmTable(**osrm_res)

    async def match(
            self,
            coordinates: List[model.Point],
            profile: Optional[str] = None,
            steps: bool = False,
            geometries: str = 'polyline',
            annotations: bool = False,
            overview: str = 'simplified',
            timestamps: List[int] = [],
            radiuses: List[float] = [],
    ) -> model.OsrmMatch:
        """OSRM Match service.

        Map matching matches/snaps given GPS points to the road network in the
        most plausible way. Please note the request might result multiple
        sub-traces. Large jumps in the timestamps (> 60s) or improbable
        transitions lead to trace splits if a complete matching could not be
        found. The algorithm might not be able to match all points. Outliers
        are removed if they can not be matched successfully.

        See http://project-osrm.org/docs/v5.5.1/api/#match-service

        :param coordinates: List of coordinates.
        :keyword profile: OSRM Profile, defaults to client default.
        :keyword steps: Return route steps for each route.
        :keyword geometries: Returned route geometry format.
        :keyword annotations: Returns additional metadata for each coordinate.
        :keyword overview: Add overview geometry
        :keyword timestamps: UNIX Timestamps (seconds) for the input locations.
        :keyword radiuses: Stddev of GPS precision used for map matching.

        :return: Match computed by OSRM.
        :rtype: ~model.OsrmMatch
        """
        osrm_res = await self._osrm_service(
            'match', profile, coordinates,
            steps=steps,
            geometries=geometries,
            annotations=annotations,
            overview=overview,
            timestamps=timestamps,
            radiuses=radiuses,
        )
        return model.OsrmMatch(**osrm_res)

    async def trip(
            self,
            coordinates: List[model.Point],
            profile: Optional[str] = None,
            steps: bool = False,
            annotations: bool = False,
            geometries: str = 'polyline',
            overview: str = 'simplified',
            source: str = 'any',
            destination: str = 'any',
    ) -> model.OsrmTrip:
        """OSRM Trip service.

        The trip plugin solves the Traveling Salesman Problem using a
        greedy heuristic (farthest-insertion algorithm). The returned
        path does not have to be the fastest path, as TSP is NP-hard
        it is only an approximation. Note that if the input
        coordinates can not be joined by a single trip (e.g. the
        coordinates are on several disconnected islands) multiple
        trips for each connected component are returned.

        See http://project-osrm.org/docs/v5.5.1/api/#trip-service

        :param coordinates: List of coordinates.
        :keyword profile: OSRM Profile, defaults to client default.
        :keyword steps: Return route steps for each route leg.
        :keyword annotations: Returns additional metadata for each coordinate.
        :keyword geometries: Returned route geometry format.
        :keyword overview: Add overview geometry.

        :keyword source: Source type, use SourceType.FIRST to set first
                         coordinate as source
        :keyword destination: Destination type, use DestinationTypeyLAST
                               to setlast coordinate as destination

        :returns: Trip calculated by OSRM.
        :rtype: ~model.OsrmTrip
        """
        osrm_res = await self._osrm_service(
            'trip', profile, coordinates,
            steps=steps,
            geometries=geometries,
            overview=overview,
            annotations=annotations,
            source=source.value,
            destination=destination.value,
        )
        print(osrm_res)
        return model.OsrmTrip(**osrm_res)

    async def tile(
            self,
            x: float,
            y: float,
            zoom: float,
    ) -> model.OsrmTile:
        """OSRM Tile service.

        This service generates Mapbox Vector Tiles that can be viewed
        with a vector-tile capable slippy-map viewer. The tiles
        contain road geometries and metadata that can be used to
        examine the routing graph. The tiles are generated directly
        from the data in-memory, so are in sync with actual routing
        results, and let you examine which roads are actually
        routable, and what weights they have applied.  The x, y, and
        zoom values are the same as described at
        https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames, and
        are supported by vector tile viewers like Mapbox GL JS.

        See http://project-osrm.org/docs/v5.5.1/api/#tile-service

        :param x: X tile
        :param y: Y tile
        :param zoom: Zoom requested

        :return: Tile
        :rtype: ~model.OsrmTile
        """
        url = f'/tile/{self.api_version}/driving/({x},{y},{zoom}).mvt'
        osrm_res = await self._get(url)
        return model.OsrmTile(**osrm_res)

    async def _osrm_service(
            self,
            service: str,
            profile: str,
            coordinates: List[model.Point],
            **kwargs,
    ) -> dict:
        """Request to a OSRM service.
        """
        url = _build_osrm_url(
            service,
            self.api_version,
            profile if profile else self.default_profile,
            coordinates,
            **kwargs
        )
        async with self._session.get(url) as res:
            res.raise_for_status()
            return await res.json()
