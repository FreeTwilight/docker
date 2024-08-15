import asyncio,time
import aiohttp
import sys,os,json,tarfile
from io import BytesIO


from docker.networks import Networks


async def main():
    networks = Networks("172.16.80.42","2376")
    try:
        body = {
            'Container': '797e30641c6d', # ID or Name
            'Force': True
        }
        ret = await networks.disconnect(network_name='my_network14',body=body)
        print(json.dumps(ret,ensure_ascii = False,indent=4))
    finally:
        await networks.close()
    
asyncio.run(main())