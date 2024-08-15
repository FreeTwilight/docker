
import asyncio,time
import aiohttp
import sys,os,json


from  docker.containers  import Containers
from  cpuinfo import CPU
async def main():
    containers = Containers("172.16.80.42","2376")
    try:
        async for log in  containers.logs(container_id = '4d03781045f6',params={"stdout": True, "stderr": True} ):
            print(log)


    finally:
        await containers.close()

    
asyncio.run(main())

