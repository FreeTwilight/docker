
import asyncio
import aiohttp
from docker.containers import Containers 
from docker.networks import Networks 
from docker.volumes import Volumes 
from docker.system import System
from docker.session import Session
from docker.exec import Exec
from docker.images import Images

class Client:
    def __init__(self,hostname,port,upgrade_h2c = False):
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=1000))
        if upgrade_h2c != False:
            pass
        self.containers = Containers(hostname = hostname,port = port,session = self.session)
        self.networks = Networks(hostname = hostname,port = port,session = self.session)
        self.volumes = Volumes(hostname = hostname,port = port,session = self.session)
        self.system = System(hostname = hostname,port = port,session = self.session)
        self.exec = Exec(hostname = hostname,port = port,session = self.session)
        self.images = Images(hostname = hostname,port = port,session = self.session)
        
        
        
    async def close(self):
        """
        Close ClientSession.
        """
        await self.session.close()
        