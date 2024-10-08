import asyncio,time
import aiohttp
import sys,os,json


from docker.images import Images

async def main():
    images = Images("172.16.80.42","2376")
    try:
        params = {
            'term':'nginx',
            'limit':10,
            'filters':json.dumps({"is-official": ["true"], "stars": ["1000"]})
        }
        ret = await images.search(params=params)
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await images.close()

    
asyncio.run(main())