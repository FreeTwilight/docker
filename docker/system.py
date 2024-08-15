import asyncio
import aiohttp
import base64,json,os
import tarfile
from io import BytesIO

class System:
    def __init__(self,hostname,port,session:aiohttp.ClientSession = None):
        if session != None:
            self.session = session 
        else:
            self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=1000))
            
        self.hostname = hostname 
        self.port = port
        self.api_url = f"http://{self.hostname}:{self.port}"
        
        
    async def close(self):
        """
        关闭 ClientSession.
        """
        await self.session.close() 
        
    async def auth(self,x_registry_auth: dict = None) -> dict:
        """
            Check auth configuration
                Validate credentials for a registry and, if available, get an identity token for accessing the registry without password.

                REQUEST BODY schema: application/json
                Authentication to check

                    username	
                        string
                    password	
                        string
                    email	
                        string
                    serveraddress	
                        string
        """
        headers = {'Content-Type': 'application/json'}
        async with self.session.post(f"{self.api_url}/auth",headers = headers,json = x_registry_auth) as response:
            if response.status != 200 and response.status != 204 and response.status != 401:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to auth {x_registry_auth['serveraddress']}",
                    headers=response.headers
                )

            return await response.json()
        
    async def info(self) -> dict:
        """
            param is none 
        """
                
        async with self.session.get(f"{self.api_url}/info") as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to get Docker system info",
                    headers=response.headers
                )

            return await response.json()
        
    async def version(self) -> dict:
        """
            param is none 
        """
                
        async with self.session.get(f"{self.api_url}/version") as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to get Docker system version",
                    headers=response.headers
                )
            return await response.json()
        
        
    async def get_ping(self) -> dict:
        """
            param is none 
        """
                
        async with self.session.get(f"{self.api_url}/_ping") as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to get Docker system ping",
                    headers=response.headers
                )
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()
        
    async def head_ping(self) -> dict:
        """
            param is none 
        """
                
        async with self.session.head(f"{self.api_url}/_ping") as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to head Docker system ping",
                    headers=response.headers
                )
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()
                
    async def monitor_events(self,params:dict=None) -> dict:
        """
            QUERY PARAMETERS
                since	
                    string
                        Show events created since this timestamp then stream new events.

                until	
                    string
                        Show events created until this timestamp then stop streaming.

                filters	
                    string
                        A JSON encoded value of filters (a map[string][]string) to process on the event list. Available filters:

                        config=<string> config name or ID
                        container=<string> container name or ID
                        daemon=<string> daemon name or ID
                        event=<string> event type
                        image=<string> image name or ID
                        label=<string> image or container label
                        network=<string> network name or ID
                        node=<string> node ID
                        plugin= plugin name or ID
                        scope= local or swarm
                        secret=<string> secret name or ID
                        service=<string> service name or ID
                        type=<string> object to filter by, one of container, image, volume, network, daemon, plugin, node, service, secret or config
                        volume=<string> volume name 
        """
                
        async with self.session.get(f"{self.api_url}/events",params=params) as response:
            if response.status != 200 and response.status != 400:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to get Docker monitor events",
                    headers=response.headers
                )
            else:
                print(response)
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    async for chunk in response.content.iter_any():
                        try:
                            yield chunk.decode('utf-8', errors='ignore')
                        except UnicodeDecodeError:
                            yield chunk.decode(errors='replace')
                else:
                    yield response.text()
        

    async def data_usage_info(self,params:dict=None) -> dict:
        """
            QUERY PARAMETERS
                type	
                    Array of strings
                        Items Enum: "container" "image" "volume" "build-cache"
                        Object types, for which to compute and return data. 
        """
                
        async with self.session.get(f"{self.api_url}/system/df",params=params) as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to get Docker data usage info",
                    headers=response.headers
                )
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()
        
