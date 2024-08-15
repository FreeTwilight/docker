
import asyncio,time
import sys,os,json


from  docker.containers  import Containers

async def main():
    containers = Containers("172.16.80.42","2376")
    try:
        await containers.export(container_id = 'e1e21a0c942d6ac6734cbadf5915372082b678ec0be18b740397e3cf68309d90')

    finally:
        await containers.close()

    
asyncio.run(main())
