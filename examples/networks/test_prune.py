import asyncio,time
import aiohttp
import sys,os,json,tarfile
from io import BytesIO


from docker.networks import Networks


async def main():
    networks = Networks("172.16.80.44","2376")
    try:
        ret = await networks.prune()
        print(json.dumps(ret,ensure_ascii = False,indent=4))
    finally:
        await networks.close()
    
asyncio.run(main())