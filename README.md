# py-osrm-client
![build](https://github.com/tomrss/py-osrm-client/actions/workflows/build.yml/badge.svg)
![publish](https://github.com/tomrss/py-osrm-client/actions/workflows/publish.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/py-osrm-client.svg)](https://badge.fury.io/py/py-osrm-client)

Simple and typed Python client for [OSRM](https://project-osrm.org/) api.

## Requirements

- [requests](https://pypi.org/project/requests/)
- [aiohttp](https://pypi.org/project/aiohttp/)


## Installation

```shell
pip install py-osrm-client
```

## Usage

Async client:

```python
import asyncio
from osrm import OsrmAsyncClient

async def example():
    async with OsrmAsyncClient() as osrm:
        coordinates = [(0.1, 0.2), (0.3, 0.4)]
        trip = await osrm.trip(coordinates)
        print(trip)

asyncio.run(example())
```


Sync client:

```python
from osrm import OsrmClient

with OsrmClient() as osrm:
    coordinates = [(0.1, 0.2), (0.3, 0.4)]
    trip = osrm.trip(coordinates)
    print(trip)
```

By default the clients will refer to the OSRM demo server at [https://router.project-osrm.org](https://router.project-osrm.org). 
To use another OSRM server:

```python
async with OsrmAsyncClient(base_url='https://my-custom-osrm-server.com') as osrm:
    # use client
```

Refer to [OSRM api documentation](https://project-osrm.org/docs/v5.24.0/api/) for more details
about OSRM services and options.
