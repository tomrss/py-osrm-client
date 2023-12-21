from unittest.mock import MagicMock

import pytest
import aiohttp

from osrm.model import ServiceStatus

pytest_plugins = ('pytest_asyncio',)

base_url = 'http://router.project-osrm.org'
api_v = 'v1'
coords = [(0.1, 0.2), (0.3, 0.4)]


@pytest.fixture
def aiohttp_mock():
    def _do_mock(status = 200, json = {}):
        mock = aiohttp.ClientSession
        mock.get = MagicMock()
        mock.get.return_value.__aenter__.return_value.status = status
        mock.get.return_value.__aenter__.return_value.json.return_value = json

    return _do_mock


@pytest.fixture
def fnearest():
    def _assertions(nearest):
        assert nearest.code == ServiceStatus.OK
        assert len(nearest.waypoints) == 2
        for i in [0, 1]:
            wp = nearest.waypoints[i]
            assert wp.name == f'thename{i}'
            assert wp.hint == f'thehint{i}'
            assert wp.distance == 433333.1

    return {
        "url": f'{base_url}/nearest/{api_v}/driving/0.1,0.2;0.3,0.4?number=1',
        "coords": coords,
        "res_json": """
        {
          "code": "Ok",
          "waypoints": [
            {
              "name": "thename0",
              "location": [0.1, 2.3],
              "distance": 433333.1,
              "hint": "thehint0"
            },
            {
              "name": "thename1",
              "location": [0.1, 2.3],
              "distance": 433333.1,
              "hint": "thehint1"
            }
          ]
        }
        """,
        "assertions": _assertions,
    }


@pytest.fixture
def froute():
    def _assertions(route):
        assert route.code == ServiceStatus.OK
        assert len(route.waypoints) == 2
        for i in [0, 1]:
            wp = route.waypoints[i]
            assert wp.name == f'thename{i}'
            assert wp.hint == f'thehint{i}'
            assert wp.distance == 433333.1
        assert len(route.routes) == 1
        r = route.routes[0]
        assert r.distance == 0.1
        assert r.legs[0].steps[0].name == "thename"
        assert r.legs[0].steps[0].maneuver.type == "blblbl"

    return {
        "url": (
            f'{base_url}/route/{api_v}/driving/0.1,0.2;0.3,0.4?'
            'alternatives=false&steps=true&geometries=polyline&'
            'overview=simplified&annotations=false&continue_straight=default'
        ),
        "coords": coords,
        "res_json": """
        {
          "code": "Ok",
          "routes": [
            {
              "distance": 0.1,
              "duration": 0.2,
              "geometry": "somepolyline",
              "legs": [
                {
                  "distance": 0.1,
                  "duration": 0.2,
                  "steps": [
                    {
                      "name": "thename",
                      "mode": "car",
                      "distance": 0.1,
                      "duration": 0.2,
                      "geometry": "otherpolyline",
                      "maneuver": {
                        "location": [1.1, 1.2],
                        "bearing_before": 32.1,
                        "bearing_after": 12.3,
                        "type": "blblbl"
                      },
                      "intersections": []
                    }
                  ]
                }
              ]
            }
          ],
          "waypoints": [
            {
              "name": "thename0",
              "location": [0.1, 2.3],
              "distance": 433333.1,
              "hint": "thehint0"
            },
            {
              "name": "thename1",
              "location": [0.1, 2.3],
              "distance": 433333.1,
              "hint": "thehint1"
            }
          ]
        }
        """,
        "assertions": _assertions,
    }


@pytest.fixture
def ftable():
    def _assertions(table):
        assert table.code == ServiceStatus.OK
        assert len(table.sources) == 2
        for i in [0, 1]:
            src = table.sources[i]
            assert src.name == f'thesource{i}'
            assert src.hint == f'thehint{i}'
            assert src.distance == 433333.1
            dest = table.destinations[i]
            assert dest.name == f'thedest{i}'
            assert dest.hint == f'thehint{i}'
            assert dest.distance == 433333.1
        assert len(table.durations) == 2
        assert len(table.durations[0]) == 2
        assert len(table.durations[1]) == 2
        assert table.durations[0][1] == 5.2

    return {
        "url": (
            f'{base_url}/table/{api_v}/driving/0.1,0.2;0.3,0.4?'
            'sources=all&destinations=all'
        ),
        "coords": coords,
        "res_json": """
        {
          "code": "Ok",
          "durations": [[5.1, 5.2], [5.2, 5.1]],
          "sources": [
            {
              "name": "thesource0",
              "location": [0.1, 2.3],
              "distance": 433333.1,
              "hint": "thehint0"
            },
            {
              "name": "thesource1",
              "location": [0.1, 2.3],
              "distance": 433333.1,
              "hint": "thehint1"
            }
          ],
          "destinations": [
            {
              "name": "thedest0",
              "location": [0.1, 2.3],
              "distance": 433333.1,
              "hint": "thehint0"
            },
            {
              "name": "thedest1",
              "location": [0.1, 2.3],
              "distance": 433333.1,
              "hint": "thehint1"
            }
          ]
        }
        """,
        "assertions": _assertions,
    }


@pytest.fixture
def fmatch():
    def _assertions(match):
        assert match.code == ServiceStatus.OK
        assert len(match.tracepoints) == 1
        tp = match.tracepoints[0]
        assert tp.name == f'thename0'
        assert tp.hint == f'thehint0'
        assert tp.distance == 433333.1
        assert len(match.matchings) == 1
        r = match.matchings[0]
        assert r.distance == 0.1
        assert r.legs[0].steps[0].name == "thename"
        assert r.legs[0].steps[0].maneuver.type == "blblbl"

    return {
        "url": (
            f'{base_url}/match/{api_v}/driving/0.1,0.2;0.3,0.4?'
            'steps=true&geometries=polyline&'
            'annotations=false&overview=simplified'
        ),
        "coords": coords,
        "res_json": """
        {
          "code": "Ok",
          "tracepoints": [
            {
              "name": "thename0",
              "location": [0.1, 2.3],
              "distance": 433333.1,
              "hint": "thehint0",
              "mathing_index": 0
            }
          ],
          "matchings": [
            {
              "distance": 0.1,
              "duration": 0.2,
              "confidence": 0.5,
              "geometry": "somepolyline",
              "legs": [
                {
                  "distance": 0.1,
                  "duration": 0.2,
                  "steps": [
                    {
                      "name": "thename",
                      "mode": "car",
                      "distance": 0.1,
                      "duration": 0.2,
                      "geometry": "otherpolyline",
                      "maneuver": {
                        "location": [1.1, 1.2],
                        "bearing_before": 32.1,
                        "bearing_after": 12.3,
                        "type": "blblbl"
                      },
                      "intersections": []
                    }
                  ]
                }
              ]
            }
          ]
        }
        """,
        "assertions": _assertions,
    }


@pytest.fixture
def ftrip():
    def _assertions(trip):
        assert trip.code == ServiceStatus.OK
        assert len(trip.waypoints) == 1
        tp = trip.waypoints[0]
        assert tp.name == f'thename0'
        assert tp.hint == f'thehint0'
        assert tp.distance == 433333.1
        assert len(trip.trips) == 1
        r = trip.trips[0]
        assert r.distance == 0.1
        assert r.legs[0].steps[0].name == "thename"
        assert r.legs[0].steps[0].maneuver.type == "blblbl"

    return {
        "url": (
            f'{base_url}/trip/{api_v}/driving/0.1,0.2;0.3,0.4?'
            'steps=true&geometries=polyline&'
            'annotations=false&overview=simplified'
        ),
        "coords": coords,
        "res_json": """
        {
          "code": "Ok",
          "waypoints": [
            {
              "name": "thename0",
              "location": [0.1, 2.3],
              "distance": 433333.1,
              "hint": "thehint0",
              "trips_index": 0,
              "waypoint_index": 0
            }
          ],
          "trips": [
            {
              "distance": 0.1,
              "duration": 0.2,
              "confidence": 0.5,
              "geometry": "somepolyline",
              "legs": [
                {
                  "distance": 0.1,
                  "duration": 0.2,
                  "steps": [
                    {
                      "name": "thename",
                      "mode": "car",
                      "distance": 0.1,
                      "duration": 0.2,
                      "geometry": "otherpolyline",
                      "maneuver": {
                        "location": [1.1, 1.2],
                        "bearing_before": 32.1,
                        "bearing_after": 12.3,
                        "type": "blblbl"
                      },
                      "intersections": []
                    }
                  ]
                }
              ]
            }
          ]
        }
        """,
        "assertions": _assertions,
    }
