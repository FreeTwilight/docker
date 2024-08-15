import asyncio,time
import aiohttp
import sys,os,json


from docker.containers import Containers

async def main():
    containers = Containers("172.16.80.41","2376")
    try:
        ret = await containers.remove(container_id="755392fbe5da")
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await containers.close()

    
asyncio.run(main())