import asyncio,time
import aiohttp
import sys,os,json


from docker.containers import Containers

async def main():
    containers = Containers("172.16.80.42","2376")
    try:
        body = {
            "BlkioWeight": 300,
            "CpuShares": 512,
            "CpuPeriod": 100000,
            "CpuQuota": 50000,
            "CpuRealtimePeriod": 1000000,
            "CpuRealtimeRuntime": 10000,
            "CpusetCpus": "0,1",
            "CpusetMems": "0",
            "Memory": 314572800,
            "MemorySwap": 514288000,
            "MemoryReservation": 209715200
        }
        ret = await containers.update(container_id="0422ccf6e4b9",body=body)
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await containers.close()

    
asyncio.run(main())