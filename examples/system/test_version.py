import asyncio
import sys,os,json


from docker.system import System


async def main():
    system = System("172.16.80.42","2376")
    try:
        ret = await system.version()
        print(json.dumps(ret,ensure_ascii = False,indent=4))
    finally:
        await system.close()
    
asyncio.run(main())