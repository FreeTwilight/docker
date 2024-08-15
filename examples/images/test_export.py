
import asyncio,time
import aiohttp
import sys,os,json


from  images  import Images

async def main():
    images = Images("172.16.80.35","2376")
    try:
        await images.export(image_name = 'hub.thifly.com:5443/center-graph/webyu:6.16')
        # async for log in  images.export(image_name = 'hub.thifly.com:5443/center-graph/webyu:6.16'):
            
        #     print(log)

        
    finally:
        await images.close()

    
asyncio.run(main())
