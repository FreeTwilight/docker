import asyncio,time
import aiohttp
import sys,os,json


from docker.exec import Exec

async def main():
    containers_exec = Exec("172.16.80.42","2376")
    try:
        params = {
            "Cmd": ["echo", "Hello, World!"],
            "AttachStdout": True,
            "AttachStderr": True,
            "Tty": False
        }
        ret = await containers_exec.create(container_id="4d03781045f6",params=params)
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await containers_exec.close()

    
asyncio.run(main())