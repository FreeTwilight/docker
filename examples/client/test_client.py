import asyncio,time
import aiohttp
import sys,os,json,tarfile
from io import BytesIO


from docker.client import Client


async def main():
    client = Client("172.16.80.42","2376")
    try:
        ret = await client.networks.list()
        print(json.dumps(ret,ensure_ascii = False,indent=4))
    finally:
        await client.close()
    
asyncio.run(main())