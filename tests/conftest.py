import pytest

from osrm.model import ServiceStatus

pytest_plugins = ('pytest_asyncio',)

base_url = 'http://router.project-osrm.org'
api_v = 'v1'
coords = [(0.1, 0.2), (0.3, 0.4)]


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
