import asyncio,time
import aiohttp
import sys,os,json


from docker.exec import Exec

async def main():
    containers_exec = Exec("172.16.80.42","2376")
    try:
        async for log in containers_exec.start(
                instance_id="5132f9e51260100066b21205feb38fd8a17b27e820cc99b506261f85990b4aff",
                body = {
                    "Detach": False,
                    "Tty": True,
                    "ConsoleSize": [
                        80,
                        64
                    ]
                    }
                ):
            print(log)
        
        
    finally:
        await containers_exec.close()

    
asyncio.run(main())