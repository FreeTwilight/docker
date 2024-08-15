import asyncio
import aiohttp
import base64,json,os
import tarfile
from io import BytesIO
class Networks:
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
        Returns a list of networks. For details on the format, see the network inspect endpoint.

        Note that it uses a different, smaller representation of a network than inspecting a single network. 
        For example, the list of containers attached to the network is not propagated in API versions 1.28 and up.
        
        QUERY PARAMETERS

        filters	
            string
                JSON encoded value of the filters (a map[string][]string) to process on the networks list.

        Available filters:

            dangling=<boolean> When set to true (or 1), returns all networks that are not in use by a container. When set to false (or 0), only networks that are in use by one or more containers are returned.
            driver=<driver-name> Matches a network's driver.
            id=<network-id> Matches all or part of a network ID.
            label=<key> or label=<key>=<value> of a network label.
            name=<network-name> Matches all or part of a network name.
            scope=["swarm"|"global"|"local"] Filters networks by scope (swarm, global, or local).
            type=["custom"|"builtin"] Filters networks by type. The custom keyword returns all user-defined networks.
        """
        async with self.session.get(f"{self.api_url}/networks",params=params) as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Failed to query docker networks",
                    headers=response.headers
                )
            return await response.json()
        
    async def inspect(self,network_name,params: dict = None):
        """
        Returns a list of networks. For details on the format, see the network inspect endpoint.

        Note that it uses a different, smaller representation of a network than inspecting a single network. 
        For example, the list of containers attached to the network is not propagated in API versions 1.28 and up.
        
        PATH PARAMETERS
            network_name
                required
                    string
                        Network ID or name

        QUERY PARAMETERS
            verbose	
                boolean
                    Default: false
                    Detailed inspect output for troubleshooting

            scope	
                string
                    Filter the network by scope (swarm, global, or local)
        """
        
        async with self.session.get(f"{self.api_url}/networks/{network_name}",params=params) as response:
            if response.status != 200 and response.status != 404:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Failed to inspect docker network",
                    headers=response.headers
                )
            return await response.json()
        
    async def remove (self,network_name,params: dict = None):
        """
        Returns a list of networks. For details on the format, see the network inspect endpoint.

        Note that it uses a different, smaller representation of a network than inspecting a single network. 
        For example, the list of containers attached to the network is not propagated in API versions 1.28 and up.
        
        PATH PARAMETERS
            network_name
                required
                    string
                        Network ID or name

        """
        
        async with self.session.delete(f"{self.api_url}/networks/{network_name}",params=params) as response:
            if response.status != 204 and response.status != 403 and response.status != 404:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Failed to delete docker network",
                    headers=response.headers
                )
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()
        
        
    async def create(self,body: dict = None):
        """
            Request Body schema: application/json
            required
            Network configuration

                Name
                    required
                    string
                        The network's name.

                CheckDuplicate	
                    boolean
                        Deprecated: CheckDuplicate is now always enabled.

                Driver	
                    string
                        Default: "bridge"
                        Name of the network driver plugin to use.

                Scope	
                    string
                        The level at which the network exists (e.g. swarm for cluster-wide or local for machine level).

                Internal	
                    boolean
                        Restrict external access to the network.

                Attachable	
                    boolean
                        Globally scoped network is manually attachable by regular containers from workers in swarm mode.

                Ingress	
                    boolean
                        Ingress network is the network which provides the routing-mesh in swarm mode.

                ConfigOnly	
                    boolean
                        Default: false
                        Creates a config-only network. Config-only networks are placeholder networks for network configurations to be used by other networks. Config-only networks cannot be used directly to run containers or services.

                ConfigFrom	
                    object (ConfigReference)
                        The config-only network source to provide the configuration for this network.

                IPAM	
                    object (IPAM)
                EnableIPv6	
                    boolean
                        Enable IPv6 on the network.

                Options	
                    object
                        Network specific options to be used by the drivers.

                Labels	
                    object
                        User-defined key/value metadata.

        """
        async with self.session.post(f"{self.api_url}/networks/create",json=body) as response:
            if response.status != 200 and response.status != 201 and response.status != 400 and response.status != 403 and response.status != 404:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Failed to create docker network",
                    headers=response.headers
                )
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()
        
        
    async def connect(self,network_name,body: dict = None):
        """
            The network must be either a local-scoped network or a swarm-scoped network with the attachable option set. A network cannot be re-attached to a running container

            PATH PARAMETERS
                id
                    required
                        string
                        Network ID or name

            REQUEST BODY SCHEMA: application/json
                required
                        Container	
                            string
                            The ID or name of the container to connect to the network.

                        EndpointConfig	
                            object (EndpointSettings)
                            Configuration for a network endpoint.

        """
        
        async with self.session.post(f"{self.api_url}/networks/{network_name}/connect",json=body) as response:
            if response.status != 200 and response.status != 400 and response.status != 403 and response.status != 404:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Failed to connect Docker network",
                    headers=response.headers
                )
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()

    async def disconnect(self,network_name,body: dict = None):
        """
            PATH PARAMETERS
                id
                    required
                    string
                    Network ID or name

            REQUEST BODY SCHEMA: application/json
                required
                    Container	
                        string
                        The ID or name of the container to disconnect from the network.

                    Force	
                        boolean
                        Force the container to disconnect from the network.

        """
        
        async with self.session.post(f"{self.api_url}/networks/{network_name}/disconnect",json=body) as response:
            if response.status != 200 and response.status != 403 and response.status != 404:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Failed to disconnect Docker network",
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
            Delete unused networks

            QUERY PARAMETERS

            filters	
                string
                    Filters to process on the prune list, encoded as JSON (a map[string][]string).

            Available filters:

                until=<timestamp> Prune networks created before this timestamp. The <timestamp> can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g. 10m, 1h30m) computed relative to the daemon machine’s time.
                label (label=<key>, label=<key>=<value>, label!=<key>, or label!=<key>=<value>) Prune networks with (or without, in case label!=... is used) the specified labels.

        """
        
        async with self.session.post(f"{self.api_url}/networks/prune",params=params) as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Failed to delete Docker network",
                    headers=response.headers
                )
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()