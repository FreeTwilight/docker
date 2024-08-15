
import asyncio,time
import aiohttp
import sys,os,json


from  images  import Images

async def main():
    images = Images("172.16.80.42","2376")
    try:

        async for log in  images.push(image_name = 'hub.thifly.com:5443/center-graph/webyu:6.16.1',
                                x_registry_auth = {
                                        "username": "cicd",
                                        "password": "CiCd!1234",
                                        "email": "string",
                                        "serveraddress": "string"
                                        } ):
            
            try:
                print(json.dumps(json.loads(log),ensure_ascii = False,indent=4))
            except (ValueError, TypeError):
                pass
        
    finally:
        await images.close()

    
asyncio.run(main())
