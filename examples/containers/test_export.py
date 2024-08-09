
import asyncio,time
import sys,os,json

sys.path.append(os.path.join(os.getcwd(), "docker"))
from  containers  import Containers

async def main():
    containers = Containers("172.16.80.42","2376")
    await containers.init_session()
    try:
        await containers.export(container_id = 'e1e21a0c942d6ac6734cbadf5915372082b678ec0be18b740397e3cf68309d90')

    finally:
        await containers.close()

    
asyncio.run(main())
