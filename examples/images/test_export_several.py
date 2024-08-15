import asyncio,time
import aiohttp
import sys,os,json


from docker.images import Images

async def main():
    images = Images("172.16.80.42","2376")
    try:
        params = {
            'names':['searxng/searxng-test-01:latest','searxng/searxng-test:latest'],
            'target_dir':'/home/bigdata/lljing/export-iamges',
            'filename':'test_exports'
            }
        await images.exports(params=params)
        
    finally:
        await images.close()

    
asyncio.run(main())