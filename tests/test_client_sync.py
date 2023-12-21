import json

from osrm import OsrmClient


def test_nearest(fnearest, requests_mock):
    requests_mock.get(fnearest["url"], json=json.loads(fnearest["res_json"]))

    with OsrmClient() as osrm:
        nearest = osrm.nearest(fnearest["coords"])

    fnearest["assertions"](nearest)


def test_route(froute, requests_mock):
    requests_mock.get(froute["url"], json=json.loads(froute["res_json"]))

    with OsrmClient() as osrm:
        route = osrm.route(froute["coords"], steps=True)

    froute["assertions"](route)
