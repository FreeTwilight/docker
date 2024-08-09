import asyncio,time
import aiohttp
import sys,os,json

sys.path.append(os.path.join(os.getcwd(), "docker"))
from containers import Containers

async def main():
    containers = Containers("172.16.80.41","2376")
    await containers.init_session()
    try:
        # 定义过滤器来仅清理具有特定标签的容器
        filters = {
            "label": ["environment=production"]
        }
        ret = await containers.prune(params=filters)
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await containers.close()

    
asyncio.run(main())