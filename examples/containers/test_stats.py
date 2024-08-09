
import asyncio,time
import aiohttp
import sys,os,json

sys.path.append(os.path.join(os.getcwd(), "docker"))
from  containers  import Containers
from  cpuinfo import CPU
async def main():
    containers = Containers("172.16.80.42","2376")
    await containers.init_session()
    try:
        async for stats in  containers.stats(container_id = 'e1e21a0c942d6ac6734cbadf5915372082b678ec0be18b740397e3cf68309d90'):
            print(json.dumps(stats,ensure_ascii = False,indent=4))
            cpu = CPU(stats['cpu_stats'],stats['precpu_stats'])
            print(f"CPU Usage: {cpu.calc_cpu_percent():.2f}%")

    finally:
        await containers.close()

    
asyncio.run(main())

