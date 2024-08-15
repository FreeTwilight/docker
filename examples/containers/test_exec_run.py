import asyncio,time
import aiohttp
import sys,os,json


from docker.containers import Containers

async def main():
    containers = Containers("172.16.80.42","2376")
    try:
        body = {
            "Cmd": ["echo", "Hello, World!"],
            "AttachStdout": True,
            "AttachStderr": True,
            "Tty": False
        }
        ret = await containers.exec_run(container_id="4d03781045f6",body=body)
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await containers.close()

    
asyncio.run(main())