import asyncio,time
import aiohttp
import sys,os,json,tarfile
from io import BytesIO


from docker.images import Images

async def main():
    images = Images("172.16.80.44","2376")
    try:
        params = {
            'from_dir':'/home/bigdata/lljing/export-iamges',
            'filename':'test_exports.tar'
        }
        async for log in  images.load(params=params):
            print(log)
    finally:
        await images.close()

    
asyncio.run(main())