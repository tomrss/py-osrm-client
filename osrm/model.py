import enum
from typing import (
    Optional,
    List,
    Tuple,
    Union,
)


# type alias for point as couple (longitude, latitude)
Point = Tuple[float, float]


class BaseModel():
    def __init__(self, **data):
        for key, value in data.items():
            setattr(self, key, value)


# Result objects

class ResultObject(BaseModel):
    """Base OSRM result object.

    See http://project-osrm.org/docs/v5.5.1/api/#result-objects
    """


class Annotation(ResultObject):
    """Annotation of the whole route leg with fine-grained information
    about each segment or node id.

    See http://project-osrm.org/docs/v5.5.1/api/#annotation-object
    """
    distance: List[float]
    duration: List[float]
    datasources: List[int]
    nodes: List[int]


class Waypoint(ResultObject):
    """Object used to describe waypoint on a route.

    See http://project-osrm.org/docs/v5.5.1/api/#waypoint-object
    """
    name: str
    location: Point
    distance: float
    hint: str
    # needed by trip service
    trips_index: Optional[int] = None
    # needed by trip and match services
    waypoint_index: Optional[int] = None
    # needed by match service
    matchings_index: Optional[int] = None


class Lane(ResultObject):
    """A Lane represents a turn lane at the corresponding turn location.

    See http://project-osrm.org/docs/v5.5.1/api/#lane-object
    """
    indications: List[str]
    valid: bool


class Intersection(ResultObject):
    """An intersection gives a full representation of any cross-way
    the path passes bay. For every step, the very first intersection
    (intersections[0]) corresponds to the location of the
    StepManeuver. Further intersections are listed for every cross-way
    until the next turn instruction.

    See http://project-osrm.org/docs/v5.5.1/api/#intersection-object
    """
    location: Point
    bearings: List[float]
    entry: List[Union[str, bool]]
    # in: int
    out: int
    lanes: List[Lane]

    def __init__(self, **data):
        complex_fields = ["lanes"]
        simple_data = {
            key: val
            for key, val in data.items()
            if key not in complex_fields
        }
        super().__init__(**simple_data)
        self.lanes = [Lane(**lane) for lane in data["lanes"]]


class StepManeuver(ResultObject):
    """Step maneuver.

    See http://project-osrm.org/docs/v5.5.1/api/#stepmaneuver-object
    """
    location: Point
    bearing_before: float
    bearing_after: float
    type: str
    modifier: Optional[str] = None
    exit: Optional[int] = None


class RouteStep(ResultObject):
    """A step consists of a maneuver such as a turn or merge, followed
    by a distance of travel along a single way to the subsequent step.

    See http://project-osrm.org/docs/v5.5.1/api/#routestep-object
    """
    name: str
    mode: str
    distance: float
    duration: float
    geometry: Union[str, dict]
    ref: Union[str, int, float, None] = None
    pronunciation: Optional[str] = None
    maneuver: StepManeuver
    intersections: List[Intersection]

    def __init__(self, **data):
        complex_fields = ["maneuver", "intersections"]
        simple_data = {
            key: val
            for key, val in data.items()
            if key not in complex_fields
        }
        super().__init__(**simple_data)
        self.maneuver = StepManeuver(**data["maneuver"])
        self.intersections = [
            Intersection(**ins)
            for ins in data["intersections"]
        ]


class RouteLeg(ResultObject):
    """Represents a route between two waypoints.

    See http://project-osrm.org/docs/v5.5.1/api/#routeleg-object
    """
    distance: float
    duration: float
    summary: Optional[str] = None
    steps: List[RouteStep]
    annotation: Optional[Annotation] = None

    def __init__(self, **data):
        complex_fields = ["steps", "annotations"]
        simple_data = {
            key: val
            for key, val in data.items()
            if key not in complex_fields
        }
        super().__init__(**simple_data)
        self.steps = [RouteStep(**step) for step in data["steps"]]
        annotation = data.get("annotation", None)
        if annotation:
            self.annotation = Annotation(**data["annotation"])


class Route(ResultObject):
    """Represents a route through (potentially multiple) waypoints.

    See http://project-osrm.org/docs/v5.5.1/api/#route-object
    """
    distance: float
    duration: float
    geometry: Union[str, dict]
    legs: List[RouteLeg]
    # needed by match service
    confidence: Optional[float] = None

    def __init__(self, **data):
        complex_fields = ["legs"]
        simple_data = {
            key: val
            for key, val in data.items()
            if key not in complex_fields
        }
        super().__init__(**simple_data)
        self.legs = [RouteLeg(**leg) for leg in data["legs"]]


# Service responses

class ServiceStatus(enum.Enum):
    """Result status of any service.

    Ok 	            Request could be processed as expected.
    InvalidUrl 	    URL string is invalid.
    InvalidService 	Service name is invalid.
    InvalidVersion 	Version is not found.
    InvalidOptions 	Options are invalid.
    InvalidQuery 	The query string is synctactically malformed.
    InvalidValue 	The successfully parsed query parameters are invalid.
    NoSegment 	    One of the input coords could not snap to street segment.
    TooBig 	        Request size violates one of the service size restrictions.

    See http://project-osrm.org/docs/v5.5.1/api/#responses
    """
    OK = "Ok"
    INVALID_URL = "InvalidUrl"
    INVALID_SERVICE = "InvalidService"
    INVALID_VERSION = "InvalidVersion"
    INVALID_OPTIONS = "InvalidOptions"
    INVALID_QUERY = "InvalidQuery"
    INVALID_VALUE = "InvalidValue"
    NO_SEGMENT = "NoSegment"
    TOO_BIG = "TooBig"


class ServiceResponse(BaseModel):
    """Base response of an OSRM service.

    See http://project-osrm.org/docs/v5.5.1/api/#services
    """
    code: ServiceStatus

    def __init__(self, code: str):
        self.code = ServiceStatus(code)


class OsrmTrip(ServiceResponse):
    """Response of the OSRM Trip service.

    See http://project-osrm.org/docs/v5.5.1/api/#trip-service
    """
    waypoints: List[Waypoint]
    trips: List[Route]

    def __init__(self, **data):
        super().__init__(data["code"])
        self.waypoints = [Waypoint(**wp) for wp in data["waypoints"]]
        self.trips = [Route(**route) for route in data["trips"]]


class OsrmTable(ServiceResponse):
    """Response of the OSRM Table service

    See http://project-osrm.org/docs/v5.5.1/api/#table-service
    """
    durations: List[List[float]]
    sources: List[Waypoint]
    destinations: List[Waypoint]

    def __init__(self, **data):
        super().__init__(data["code"])
        self.durations = data["durations"]
        self.sources = [Waypoint(**wp) for wp in data["sources"]]
        self.destinations = [Waypoint(**wp) for wp in data["destinations"]]


class OsrmNearest(ServiceResponse):
    """Response of the OSRM Nearest service.

    See http://project-osrm.org/docs/v5.5.1/api/#nearest-service
    """
    waypoints: List[Waypoint]

    def __init__(self, **data):
        super().__init__(data["code"])
        self.waypoints = [Waypoint(**wp) for wp in data["waypoints"]]


class OsrmRoute(ServiceResponse):
    """Response of the OSRM Route service.

    See http://project-osrm.org/docs/v5.5.1/api/#route-service
    """
    waypoints: List[Waypoint]
    routes: List[Route]

    def __init__(self, **data):
        super().__init__(data["code"])
        self.waypoints = [Waypoint(**wp) for wp in data["waypoints"]]
        self.routes = [Route(**route) for route in data["routes"]]


class OsrmMatch(ServiceResponse):
    """Response of the OSRM Match service.

    See http://project-osrm.org/docs/v5.5.1/api/#match-service
    """
    tracepoints: List[Waypoint]
    matchings: List[Route]

    def __init__(self, **data):
        super().__init__(data["code"])
        self.tracepoints = [Waypoint(**wp) for wp in data["tracepoints"]]
        self.matchings = [Route(**route) for route in data["matchings"]]


class OsrmTile(ServiceResponse):
    """Response of the OSRM Tile service.

    See http://project-osrm.org/docs/v5.5.1/api/#tile-service
    """
    # TODO
