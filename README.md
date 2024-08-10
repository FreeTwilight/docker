# Docker SDK for Python
The docker python client supports asynchronous parallel access to containers.

Develop with Docker Engine SDKs
Docker provides an API for interacting with the Docker daemon (called the Docker Engine API), as well as SDKs for Go and Python. The SDKs allow you to efficiently build and scale Docker apps and solutions. If Go or Python don't work for you, you can use the Docker Engine API directly.

# Reference Docs
This site was built using [Dokcer Docs manuals](https://docs.docker.com/manuals/).

# Installation
The latest stable version is available on PyPI. Install with pip:
```
pip install docker-sdk
```

# Usage 
### 1. Example docker run
```
import asyncio,time
import sys,os,json

from docker.containers import Containers

async def main():
    containers = Containers("172.16.80.42","2376")
    await containers.init_session()
    try:

        ret = await containers.run(params={ "name": "hello9"},body = {'Image': 'searxng/searxng:latest'})
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await containers.close()

    
asyncio.run(main())
```
### 2. Example docker list
```
import asyncio,time
import sys,os,json

from  docker.containers  import Containers

async def main():
    containers = Containers("172.16.80.42","2376")
    await containers.init_session()
    try:
        ret = await containers.list(params = {"all":"true"})
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await containers.close()

    
asyncio.run(main())
```
