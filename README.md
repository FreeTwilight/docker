# Docker
The docker python client supports asynchronous parallel access to containers.
# Reference Docs
This site was built using [Dokcer Docs manuals](https://docs.docker.com/manuals/).

# Example docker run
```
import asyncio,time
import aiohttp
import sys,os,json

sys.path.append(os.path.join(os.getcwd(), "docker"))
from containers import Containers

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
