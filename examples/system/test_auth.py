import asyncio,time
import aiohttp
import sys,os,json


from docker.system import System

async def main():
    system = System("172.16.80.42","2376")
    try:

        ret = await system.auth(
            x_registry_auth= {
                "username": "cxxxicd",
                "password": "xxx!1234",
                "serveraddress": "https://hub.xxxx.com:5443"
            }
        )
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await system.close()

    
asyncio.run(main())