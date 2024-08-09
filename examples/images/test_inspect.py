
import asyncio,time
import aiohttp
import sys,os,json

sys.path.append(os.path.join(os.getcwd(), "docker"))
from  images  import Images

async def main():
    images = Images("172.16.80.42","2376")
    try:
        ret = await images.inspect(image_name = 'hub.thifly.com:5443/center-graph/webyu:6.16')
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await images.close()

    
asyncio.run(main())
