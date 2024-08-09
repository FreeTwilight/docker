import asyncio,time
import aiohttp
import sys,os,json

sys.path.append(os.path.join(os.getcwd(), "docker"))
from containers import Containers

async def main():
    containers = Containers("172.16.80.42","2376")
    await containers.init_session()
    try:
        params = {
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
        ret = await containers.update(container_id="0422ccf6e4b9",params=params)
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await containers.close()

    
asyncio.run(main())