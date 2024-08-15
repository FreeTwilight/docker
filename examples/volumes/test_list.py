import asyncio,time
import aiohttp
import sys,os,json,tarfile
from io import BytesIO


from docker.volumes import Volumes


async def main():
    volumes = Volumes("172.16.80.42","2376")
    try:
        ret = await volumes.list()
        print(json.dumps(ret,ensure_ascii = False,indent=4))
    finally:
        await volumes.close()
    
asyncio.run(main())