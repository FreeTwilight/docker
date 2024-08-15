import asyncio,time
import aiohttp
import sys,os,json,tarfile
from io import BytesIO


from docker.networks import Networks


async def main():
    networks = Networks("172.16.80.42","2376")
    try:
        body = {
            "Name": "my_network17",
            "CheckDuplicate": True,
            "Driver": "bridge",
            "Scope": "local",
            "Labels": {
                "com.example.some-label": "some-value",
                "com.example.some-other-label": "some-other-value"
            }
        }
        ret = await networks.create(body=body)
        print(json.dumps(ret,ensure_ascii = False,indent=4))
    finally:
        await networks.close()
    
asyncio.run(main())