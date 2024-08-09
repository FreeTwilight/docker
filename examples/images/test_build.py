import asyncio,time
import aiohttp
import sys,os,json,tarfile
from io import BytesIO

sys.path.append(os.path.join(os.getcwd(), "docker"))
from images import Images


async def main():
    images = Images("172.16.80.42","2376")
    try:
        async for log in  images.build(params={
                                    'dockerfile':'Dockerfile',
                                    'context_dir':'/home/bigdata/lljing/build-images/center-annotation',
                                    't':'test-hello:1.0.123'
                                },
                                 x_registry_config = {
                                    "hub.thifly.com:5443" : {
                                        "username":"cicd",
                                        "password":"CiCd!1234"
                                        }
                                    }
                                 ):
            
            print(log)
    finally:
        await images.close()

    
asyncio.run(main())