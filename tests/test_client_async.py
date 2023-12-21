import json
import pytest

from osrm import OsrmAsyncClient


@pytest.mark.asyncio
async def test_nearest(fnearest, aiohttp_mock):
    aiohttp_mock(json=json.loads(fnearest["res_json"]))

    async with OsrmAsyncClient() as osrm:
        nearest = await osrm.nearest(fnearest["coords"])

    fnearest["assertions"](nearest)


@pytest.mark.asyncio
async def test_route(froute, aiohttp_mock):
    aiohttp_mock(json=json.loads(froute["res_json"]))

    async with OsrmAsyncClient() as osrm:
        route = await osrm.route(froute["coords"], steps=True)

    froute["assertions"](route)


@pytest.mark.asyncio
async def test_table(ftable, aiohttp_mock):
    aiohttp_mock(json=json.loads(ftable["res_json"]))

    async with OsrmAsyncClient() as osrm:
        table = await osrm.table(ftable["coords"])

    ftable["assertions"](table)


@pytest.mark.asyncio
async def test_match(fmatch, aiohttp_mock):
    aiohttp_mock(json=json.loads(fmatch["res_json"]))

    async with OsrmAsyncClient() as osrm:
        match = await osrm.match(fmatch["coords"], steps=True)

    fmatch["assertions"](match)


@pytest.mark.asyncio
async def test_trip(ftrip, aiohttp_mock):
    aiohttp_mock(json=json.loads(ftrip["res_json"]))

    async with OsrmAsyncClient() as osrm:
        trip = await osrm.trip(ftrip["coords"], steps=True)

    ftrip["assertions"](trip)
