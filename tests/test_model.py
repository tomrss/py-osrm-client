import json

import osrm


def test_annotation():
    ann_json = """
    {
      "distance": [1.2, 1.3],
      "duration": [9.8, 9.1],
      "datasources": [0],
      "nodes": [91, 92, 99, 1000]
    }
    """
    ann_data = json.loads(ann_json)
    ann = osrm.Annotation(**ann_data)
    # ann = osrm.model.from_dict(osrm.Annotation, ann_data)

    assert len(ann.distance) == 2
    assert ann.distance[0] == 1.2
    assert ann.distance[1] == 1.3
    assert len(ann.duration) == 2
    assert ann.duration[0] == 9.8
    assert ann.duration[1] == 9.1
    assert len(ann.datasources) == 1
    assert ann.datasources[0] == 0
    assert len(ann.nodes) == 4
    assert ann.nodes[0] == 91
    assert ann.nodes[1] == 92
    assert ann.nodes[2] == 99
    assert ann.nodes[3] == 1000


def test_waypoint():
    wp_json = """
    {
      "name": "thename",
      "location": [0.1, 2.3],
      "distance": 433333.1,
      "hint": "thehint",
      "trips_index": 12
    }
    """
    wp_data = json.loads(wp_json)
    wp = osrm.Waypoint(**wp_data)

    assert wp.name == "thename"
    assert len(wp.location) == 2
    assert wp.location[0] == 0.1
    assert wp.location[1] == 2.3
    assert wp.distance == 433333.1
    assert wp.hint == "thehint"
    assert wp.trips_index == 12


def test_lane():
    lane_json = """
    {
      "indications": ["one", "two"],
      "valid": false
    }
    """
    lane_data = json.loads(lane_json)
    lane = osrm.Lane(**lane_data)

    assert len(lane.indications) == 2
    assert lane.indications[0] == "one"
    assert lane.indications[1] == "two"
    assert not lane.valid


def test_intersection():
    isec_json = """
    {
      "location": [0.1, 2.3],
      "bearings": [],
      "entry": [false, true],
      "out": 1,
      "lanes": [
        {
          "indications": ["one", "two"],
          "valid": false
        }
      ]
    }
    """
    isec_data = json.loads(isec_json)
    isec = osrm.Intersection(**isec_data)

    assert len(isec.location) == 2
    assert isec.location[0] == 0.1
    assert isec.location[1] == 2.3
    assert len(isec.entry) == 2
    assert not isec.entry[0]
    assert isec.entry[1]
    assert isec.out == 1
    assert len(isec.lanes) == 1
    lane = isec.lanes[0]
    assert len(lane.indications) == 2
    assert lane.indications[0] == "one"
    assert lane.indications[1] == "two"
    assert not lane.valid


def test_route():
    route_json = """
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
    """
    route_data = json.loads(route_json)
    route = osrm.Route(**route_data)

    assert route.distance == 0.1
    assert route.legs[0].distance == 0.1
    assert route.legs[0].steps[0].geometry == "otherpolyline"
    assert route.legs[0].steps[0].maneuver.bearing_before == 32.1
