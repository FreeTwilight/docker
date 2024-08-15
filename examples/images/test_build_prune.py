import asyncio,time
import aiohttp
import sys,os,json


from docker.images import Images

async def main():
    images = Images("172.16.80.43","2376")
    try:
        params = {
            'all': 'true'  # 删除所有类型的构建缓存
            # 'keep-storage': 1024 * 1024 * 100,  # 保留 100 MB 的磁盘空间大小
            # 'filters': json.dumps({
            #     #'until': '100h30m',  # 删除 1 小时 30 分钟前的缓存
            #     'type': 'shared'   # 只删除共享类型的缓存
            # })
        }
        ret = await images.build_prune(params=params)
        print(json.dumps(ret,ensure_ascii = False,indent=4))
        
    finally:
        await images.close()

    
asyncio.run(main())