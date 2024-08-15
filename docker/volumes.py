import asyncio
import aiohttp
import base64,json,os
import tarfile
from io import BytesIO

class Volumes:
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
        Close ClientSession.
        """
        await self.session.close()
        
        
    async def list(self,params: dict = None):
        """
        QUERY PARAMETERS
        filters	
            string <json>
                JSON encoded value of the filters (a map[string][]string) to process on the volumes list. Available filters:

                dangling=<boolean> When set to true (or 1), returns all volumes that are not in use by a container. When set to false (or 0), only volumes that are in use by one or more containers are returned.
                driver=<volume-driver-name> Matches volumes based on their driver.
                label=<key> or label=<key>:<value> Matches volumes based on the presence of a label alone or a label and a value.
                name=<volume-name> Matches all or part of a volume name.
        """
        async with self.session.get(f"{self.api_url}/volumes",params=params) as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Failed to query Docker volumes",
                    headers=response.headers
                )
            return await response.json()
        
    async def create(self,params: dict = None):
        """
        REQUEST BODY SCHEMA: application/json
        required
        Volume configuration

        Name	
            string
                The new volume's name. If not specified, Docker generates a name.

        Driver	
            string
                Default: "local"
                    Name of the volume driver to use.

        DriverOpts	
            object
                A mapping of driver options and values. These options are passed directly to the driver and are driver specific.

        Labels	
            object
                User-defined key/value metadata.

        ClusterVolumeSpec	
            object (ClusterVolumeSpec)
                Cluster-specific options used to create the volume.
        """
        
        async with self.session.post(f"{self.api_url}/volumes/create",json=params) as response:
            if response.status != 201:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Failed to create Docker volume",
                    headers=response.headers
                )
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()
                
                
    async def inspect(self,volume_name:str,params: dict = None):
        """
        PATH PARAMETERS
        name
        required
            string
                Volume name or ID
        """
        
        async with self.session.get(f"{self.api_url}/volumes/{volume_name}",params=params) as response:
            if response.status != 200 and response.status != 404:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Failed to inspect Docker volume",
                    headers=response.headers
                )
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()
            
    #todo only for swarm    
    async def update(self,volume_name:str,params: dict = None,body: dict = None):
        """
        PATH PARAMETERS
        name
        required
            string
                The name or ID of the volume

        QUERY PARAMETERS
        version
            required
                integer <int64>
                    The version number of the volume being updated. This is required to avoid conflicting writes. Found in the volume's ClusterVolume field.

        REQUEST BODY SCHEMA: application/json
            The spec of the volume to update. Currently, only Availability may change. All other fields must remain unchanged.

        Spec	
            object (ClusterVolumeSpec)
                Cluster-specific options used to create the volume.
        """
        
        async with self.session.put(f"{self.api_url}/volumes/{volume_name}",params=params,json=body) as response:
            if response.status != 200 and response.status != 400 and response.status != 404 and response.status != 503:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Failed to update Docker volume",
                    headers=response.headers
                )
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()
                
    async def remove(self,volume_name:str,params: dict = None):
        """
        Instruct the driver to remove the volume.

        PATH PARAMETERS
        name
            required
                string
                    Volume name or ID

        QUERY PARAMETERS
        force	
            boolean
                Default: false
                    Force the removal of the volume
        """
        
        async with self.session.delete(f"{self.api_url}/volumes/{volume_name}",params=params) as response:
            if response.status != 204 and response.status != 409 and response.status != 404:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Failed to update Docker volume",
                    headers=response.headers
                )
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()
                
                
    async def prune(self,params: dict = None):
        """
        QUERY PARAMETERS
        filters	
            string
                Filters to process on the prune list, encoded as JSON (a map[string][]string).

        Available filters:

            label (label=<key>, label=<key>=<value>, label!=<key>, or label!=<key>=<value>) Prune volumes with (or without, in case label!=... is used) the specified labels.
            all (all=true) - Consider all (local) volumes for pruning and not just anonymous volumes.
        """
        
        async with self.session.post(f"{self.api_url}/volumes/prune",params=params) as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Failed to prune Docker volume",
                    headers=response.headers
                )
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()
        
    