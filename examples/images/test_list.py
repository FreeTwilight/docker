import asyncio,time
import aiohttp
import sys,os,json


from docker.images import Images

async def main():
    images = Images("172.16.80.42","2376")
    try:
        ret = await images.list()
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await images.close()

    
asyncio.run(main())