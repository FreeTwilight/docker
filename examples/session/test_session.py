import asyncio,time
import aiohttp
import sys,os,json


from docker.session import Session
from docker.images import Images

async def main():
    images = Images("172.16.80.42","2376")
    s = Session("172.16.80.42","2376",images.session)
    try:

        ret = await s.init_session()
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
        ret = await images.list()
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
        
    finally:
        await s.close()

    
asyncio.run(main())