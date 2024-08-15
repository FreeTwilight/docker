import asyncio
import sys,os,json


from docker.system import System


async def main():
    system = System("172.16.80.42","2376")
    try:
        params = {
            'filters':json.dumps({'container': ['797e30641c6d']})
        }
        async for log in system.monitor_events(params=params):
            print(log)
    finally:
        await system.close()
    
asyncio.run(main())