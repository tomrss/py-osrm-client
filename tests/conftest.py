from unittest.mock import MagicMock

import pytest
import aiohttp

from osrm.model import ServiceStatus

pytest_plugins = ('pytest_asyncio',)

base_url = 'https://router.project-osrm.org'
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
        "url": f'{base_url}/nearest/{api_v}/driving/0.1,0.2?number=1',
        "coords": (0.1, 0.2),
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
def froute2():
    def _assertions(route):
        assert route.code == ServiceStatus.OK
        assert len(route.waypoints) == 2
        assert route.waypoints[0].name == 'Columbus Circle'
        assert route.waypoints[1].name == 'East 65th Street'
        assert len(route.routes) == 1
        r = route.routes[0]
        assert r.distance == 2159.9
        assert len(r.legs) == 1
        assert len(r.legs[0].steps) == 6
        assert r.legs[0].steps[0].name == "Columbus Circle"
        assert r.legs[0].steps[0].maneuver.type == "depart"
        for i in range(6):
            for j in range(len(r.legs[0].steps[i].intersections)):
                if i == 2 and j == 0:
                    assert len(r.legs[0].steps[i].intersections[j].lanes) == 3
                else:
                    assert len(r.legs[0].steps[i].intersections[j].lanes) == 0

    return {
        "url": (
            f'{base_url}/route/{api_v}/driving/'
            '-73.982155,40.767937;-73.964630,40.765602?steps=true'
        ),
        "coords": [(-73.982155, 40.767937), (-73.964630, 40.765602)],
        "res_json": r"""
{
  "code": "Ok",
  "routes": [
    {
      "legs": [
        {
          "steps": [
            {
              "intersections": [
                {
                  "out": 0,
                  "entry": [
                    true
                  ],
                  "bearings": [
                    151
                  ],
                  "location": [
                    -73.982324,
                    40.767867
                  ]
                },
                {
                  "out": 0,
                  "in": 2,
                  "entry": [
                    true,
                    false,
                    false
                  ],
                  "bearings": [
                    105,
                    225,
                    300
                  ],
                  "location": [
                    -73.982087,
                    40.767705
                  ]
                }
              ],
              "driving_side": "right",
              "maneuver": {
                "bearing_after": 151,
                "bearing_before": 0,
                "location": [
                  -73.982324,
                  40.767867
                ],
                "modifier": "left",
                "type": "depart"
              },
              "geometry": "enywFntpbMBAFGFIBEBGBK@G@E@G?S",
              "ref": "8",
              "name": "Columbus Circle",
              "mode": "driving",
              "weight": 7.5,
              "duration": 7.5,
              "distance": 45.1
            },
            {
              "intersections": [
                {
                  "out": 1,
                  "in": 2,
                  "entry": [
                    true,
                    true,
                    false
                  ],
                  "bearings": [
                    90,
                    150,
                    270
                  ],
                  "location": [
                    -73.981882,
                    40.767675
                  ]
                },
                {
                  "out": 2,
                  "in": 0,
                  "entry": [
                    false,
                    false,
                    true,
                    false
                  ],
                  "bearings": [
                    0,
                    120,
                    180,
                    300
                  ],
                  "location": [
                    -73.981749,
                    40.767135
                  ]
                }
              ],
              "driving_side": "right",
              "geometry": "_mywFvqpbMBIDGBCDEDAFCBAD?DAl@HJ@P@fAJr@HXB",
              "maneuver": {
                "exit": 1,
                "bearing_after": 151,
                "bearing_before": 92,
                "location": [
                  -73.981882,
                  40.767675
                ],
                "modifier": "right",
                "type": "exit rotary"
              },
              "name": "Broadway",
              "mode": "driving",
              "weight": 26.5,
              "duration": 26.5,
              "distance": 160
            },
            {
              "intersections": [
                {
                  "lanes": [
                    {
                      "valid": true,
                      "indications": [
                        "left"
                      ]
                    },
                    {
                      "valid": false,
                      "indications": [
                        "straight"
                      ]
                    },
                    {
                      "valid": false,
                      "indications": [
                        "none"
                      ]
                    }
                  ],
                  "out": 1,
                  "in": 0,
                  "entry": [
                    false,
                    true,
                    true,
                    true
                  ],
                  "bearings": [
                    15,
                    120,
                    180,
                    300
                  ],
                  "location": [
                    -73.981894,
                    40.766301
                  ]
                },
                {
                  "out": 1,
                  "in": 3,
                  "entry": [
                    false,
                    true,
                    true,
                    false
                  ],
                  "bearings": [
                    30,
                    120,
                    210,
                    300
                  ],
                  "location": [
                    -73.980036,
                    40.765521
                  ]
                },
                {
                  "out": 1,
                  "in": 3,
                  "entry": [
                    true,
                    true,
                    false,
                    false
                  ],
                  "bearings": [
                    30,
                    120,
                    210,
                    300
                  ],
                  "location": [
                    -73.977196,
                    40.764324
                  ]
                },
                {
                  "out": 1,
                  "in": 3,
                  "entry": [
                    false,
                    true,
                    true,
                    false
                  ],
                  "bearings": [
                    30,
                    120,
                    210,
                    300
                  ],
                  "location": [
                    -73.973974,
                    40.762972
                  ]
                },
                {
                  "out": 1,
                  "in": 3,
                  "entry": [
                    false,
                    true,
                    false,
                    false
                  ],
                  "bearings": [
                    30,
                    120,
                    210,
                    300
                  ],
                  "location": [
                    -73.972365,
                    40.762295
                  ]
                }
              ],
              "driving_side": "right",
              "geometry": "kdywFxqpbMJ_@fAiD`@oAL_@La@HUJ[pAeEjB_GXy@J[H[lAuD?ChDuKJYHWz@mCv@eCFSHWdBmFBGBKHU",
              "maneuver": {
                "bearing_after": 118,
                "bearing_before": 187,
                "location": [
                  -73.981894,
                  40.766301
                ],
                "modifier": "left",
                "type": "turn"
              },
              "name": "West 57th Street",
              "mode": "driving",
              "weight": 71.3,
              "duration": 71.3,
              "distance": 1065.9
            },
            {
              "intersections": [
                {
                  "out": 1,
                  "in": 3,
                  "entry": [
                    false,
                    true,
                    true,
                    false
                  ],
                  "bearings": [
                    30,
                    120,
                    210,
                    300
                  ],
                  "location": [
                    -73.970848,
                    40.761652
                  ]
                },
                {
                  "out": 0,
                  "in": 3,
                  "entry": [
                    true,
                    true,
                    false,
                    false
                  ],
                  "bearings": [
                    30,
                    120,
                    210,
                    300
                  ],
                  "location": [
                    -73.970671,
                    40.761578
                  ]
                },
                {
                  "out": 0,
                  "in": 2,
                  "entry": [
                    true,
                    true,
                    false,
                    false
                  ],
                  "bearings": [
                    30,
                    120,
                    210,
                    300
                  ],
                  "location": [
                    -73.970173,
                    40.762252
                  ]
                },
                {
                  "out": 0,
                  "in": 2,
                  "entry": [
                    true,
                    true,
                    false,
                    false
                  ],
                  "bearings": [
                    30,
                    120,
                    210,
                    300
                  ],
                  "location": [
                    -73.969724,
                    40.76287
                  ]
                },
                {
                  "out": 0,
                  "in": 2,
                  "entry": [
                    true,
                    false,
                    false,
                    true
                  ],
                  "bearings": [
                    30,
                    120,
                    210,
                    300
                  ],
                  "location": [
                    -73.969259,
                    40.763509
                  ]
                },
                {
                  "out": 0,
                  "in": 2,
                  "entry": [
                    true,
                    false,
                    false,
                    true
                  ],
                  "bearings": [
                    30,
                    120,
                    210,
                    300
                  ],
                  "location": [
                    -73.968805,
                    40.76413
                  ]
                },
                {
                  "out": 0,
                  "in": 2,
                  "entry": [
                    true,
                    true,
                    false,
                    false
                  ],
                  "bearings": [
                    30,
                    120,
                    210,
                    300
                  ],
                  "location": [
                    -73.968349,
                    40.764757
                  ]
                },
                {
                  "out": 0,
                  "in": 2,
                  "entry": [
                    true,
                    false,
                    false,
                    true
                  ],
                  "bearings": [
                    30,
                    120,
                    210,
                    300
                  ],
                  "location": [
                    -73.96789,
                    40.765384
                  ]
                },
                {
                  "out": 0,
                  "in": 2,
                  "entry": [
                    true,
                    true,
                    false,
                    false
                  ],
                  "bearings": [
                    30,
                    120,
                    210,
                    300
                  ],
                  "location": [
                    -73.967434,
                    40.766012
                  ]
                }
              ],
              "driving_side": "right",
              "geometry": "igxwFxlnbMLc@SM}AeAGEKIKGaBeACCIGMI}AcAECMIIG_BeAECKGKI}AcAGEKGKG}AeAGEIGMG{AcAGEKIKG}AcAGEKI",
              "maneuver": {
                "bearing_after": 118,
                "bearing_before": 118,
                "location": [
                  -73.970848,
                  40.761652
                ],
                "modifier": "left",
                "type": "turn"
              },
              "name": "Park Avenue",
              "mode": "driving",
              "weight": 96.2,
              "duration": 96.2,
              "distance": 660
            },
            {
              "intersections": [
                {
                  "out": 1,
                  "in": 2,
                  "entry": [
                    true,
                    true,
                    false,
                    false
                  ],
                  "bearings": [
                    30,
                    120,
                    210,
                    300
                  ],
                  "location": [
                    -73.966973,
                    40.766639
                  ]
                },
                {
                  "out": 1,
                  "in": 3,
                  "entry": [
                    false,
                    true,
                    true,
                    false
                  ],
                  "bearings": [
                    30,
                    120,
                    210,
                    300
                  ],
                  "location": [
                    -73.965449,
                    40.765991
                  ]
                }
              ],
              "driving_side": "right",
              "geometry": "ofywFptmbMHWlBcGHSFS~@sC",
              "maneuver": {
                "bearing_after": 118,
                "bearing_before": 28,
                "location": [
                  -73.966973,
                  40.766639
                ],
                "modifier": "right",
                "type": "turn"
              },
              "name": "East 65th Street",
              "mode": "driving",
              "weight": 27.6,
              "duration": 27.6,
              "distance": 228.9
            },
            {
              "intersections": [
                {
                  "in": 0,
                  "entry": [
                    true
                  ],
                  "bearings": [
                    299
                  ],
                  "location": [
                    -73.964607,
                    40.765633
                  ]
                }
              ],
              "driving_side": "right",
              "geometry": "e`ywFxembM",
              "maneuver": {
                "bearing_after": 0,
                "bearing_before": 119,
                "location": [
                  -73.964607,
                  40.765633
                ],
                "type": "arrive"
              },
              "name": "East 65th Street",
              "mode": "driving",
              "weight": 0,
              "duration": 0,
              "distance": 0
            }
          ],
          "weight": 229.1,
          "summary": "West 57th Street, Park Avenue",
          "duration": 229.1,
          "distance": 2159.9
        }
      ],
      "weight_name": "routability",
      "geometry": "enywFntpbMZa@L_A\\WpFb@n\\ceAs^cVhEwM",
      "weight": 229.1,
      "duration": 229.1,
      "distance": 2159.9
    }
  ],
  "waypoints": [
    {
      "hint": "aGeJhP___38DAAAABgAAADkAAAAdAAAA6GJTQEvxEUDwEkRCKQbJQQMAAAAGAAAAOQAAAB0AAAAjdgAAjB6X-3sRbgI1H5f7wRFuAhQAfwkAAAAA",
      "location": [
        -73.982324,
        40.767867
      ],
      "name": "Columbus Circle",
      "distance": 16.24735834
    },
    {
      "hint": "v2YdgP___39QAAAAkwAAAAsAAAAQAAAANb-PQmnAb0LHIhlBFqpeQVAAAACTAAAACwAAABAAAAAjdgAAwWOX-8EIbgKqY5f7oghuAgIAfwcAAAAA",
      "location": [
        -73.964607,
        40.765633
      ],
      "name": "East 65th Street",
      "distance": 3.952361071
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
