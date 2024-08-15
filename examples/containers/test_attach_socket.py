import asyncio,time
import aiohttp
import sys,os,json


from docker.containers import Containers

async def main():
    containers = Containers("172.16.80.42","2376")
    try:
        ret = await containers.attach_socket(container_id="f5b70ec06b92",params={'detachKeys':'ctrl-z'})
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await containers.close()

    
asyncio.run(main())