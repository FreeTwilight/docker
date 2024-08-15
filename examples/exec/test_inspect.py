import asyncio,time
import aiohttp
import sys,os,json


from docker.exec import Exec

async def main():
    containers_exec = Exec("172.16.80.42","2376")
    try:

        ret = await containers_exec.inspect(
            instance_id="6f4ccc3e1c98dc0c40b4ca407d3acc961562d93d6ab53caf55d22a6e079d643a"
        )
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await containers_exec.close()

    
asyncio.run(main())