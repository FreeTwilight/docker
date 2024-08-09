import asyncio,time
import aiohttp
import sys,os,json

sys.path.append(os.path.join(os.getcwd(), "docker"))
from containers import Containers

async def main():
    containers = Containers("172.16.80.42","2376")
    await containers.init_session()
    try:
        ret = await containers.attach(container_id="4d03781045f6",params={"stream":1,"stdout":1})
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await containers.close()

    
asyncio.run(main())