import asyncio,time
import aiohttp
import sys,os,json,tarfile
from io import BytesIO

sys.path.append(os.path.join(os.getcwd(), "docker"))
from images import Images


async def main():
    images = Images("172.16.80.44","2376")
    try:
        async for log in  images.create(params={
                                    'fromImage':'hub.thifly.com:5443/center-graph/blzp:v1.0.4'
                                },
                                x_registry_auth = {
                                        "username": "cicd",
                                        "password": "CiCd!1234",
                                        "email": "string",
                                        "serveraddress": "string"
                                    }
                                 ):
            
            print(log)
            
 
    finally:
        await images.close()

    
asyncio.run(main())