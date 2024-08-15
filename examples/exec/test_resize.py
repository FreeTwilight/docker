import asyncio,time
import aiohttp
import sys,os,json


from docker.exec import Exec

async def main():
    containers_exec = Exec("172.16.80.42","2376")
    try:

        ret = await containers_exec.resize(
            instance_id="8f451b5c3603f7fbdbe22f7810d87764bf9dc91d0ef7180febfe97891bf8444d",
            params= {
                "h":100,
                "w":200
            }
        )
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await containers_exec.close()

    
asyncio.run(main())