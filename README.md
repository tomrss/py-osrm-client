# py-osrm-client
![build](https://github.com/tomrss/py-osrm-client/actions/workflows/build.yml/badge.svg)

Simple Python client for [OSRM](http://project-osrm.org/) api.

## Usage

Async client:

```python
from osrm import OsrmAsyncClient

async def example():
    async with OsrmAsyncClient() as osrm:
        coordinates = [(0.1, 0.2), (0.3, 0.4)]
        trip = await osrm.trip(coordinates)
```


Sync client:

```python
from osrm import OsrmAsyncClient

async def example():
    with OsrmClient() as osrm:
        coordinates = [(0.1, 0.2), (0.3, 0.4)]
        trip = osrm.trip(coordinates)
```
