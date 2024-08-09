import asyncio,time
import aiohttp
import sys,os,json

sys.path.append(os.path.join(os.getcwd(), "docker"))
from images import Images

async def main():
    images = Images("172.16.80.42","2376")
    try:
        params = {
            'container':'0422ccf6e4b9',
            'repo':'searxng/searxng-test-01',
            'tag':'latest'    
        }
        ret = await images.commit(params=params)
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await images.close()

    
asyncio.run(main())