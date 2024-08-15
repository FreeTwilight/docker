import asyncio,time
import aiohttp
import sys,os,json


from docker.containers import Containers

async def main():
    containers = Containers("172.16.80.41","2376")
    try:
        ret = await containers.wait(container_id="1b78d00a9101")
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await containers.close()

    
asyncio.run(main())