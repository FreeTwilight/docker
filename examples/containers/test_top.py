
import asyncio,time
import aiohttp
import sys,os,json


from  docker.containers  import Containers

async def main():
    containers = Containers("172.16.80.42","2376")
    try:
        ret = await containers.top(container_id = '7d4f14a1a0b3')
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await containers.close()

    
asyncio.run(main())
