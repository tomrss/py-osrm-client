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


def test_table(ftable, requests_mock):
    requests_mock.get(ftable["url"], json=json.loads(ftable["res_json"]))

    with OsrmClient() as osrm:
        table = osrm.table(ftable["coords"])

    ftable["assertions"](table)


def test_match(fmatch, requests_mock):
    requests_mock.get(fmatch["url"], json=json.loads(fmatch["res_json"]))

    with OsrmClient() as osrm:
        match = osrm.match(fmatch["coords"], steps=True)

    fmatch["assertions"](match)


def test_trip(ftrip, requests_mock):
    requests_mock.get(ftrip["url"], json=json.loads(ftrip["res_json"]))

    with OsrmClient() as osrm:
        trip = osrm.trip(ftrip["coords"], steps=True)

    ftrip["assertions"](trip)
