import asyncio
import aiohttp
import base64,json,os
import tarfile
from io import BytesIO

from docker.containers import Containers
class Exec:
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
        await self.containers.session.close() 
        
    async def create(self,container_id:str,params: dict = None) -> dict:
        """
        Create an exec instance
            Run a command inside a running container.

            PATH PARAMETERS
                id
                    required
                        string
                        ID or name of container

            REQUEST BODY SCHEMA: application/json
            required
                Exec configuration

            AttachStdin	
                boolean
                    Attach to stdin of the exec command.

            AttachStdout	
                boolean
                    Attach to stdout of the exec command.

            AttachStderr	
                boolean
                    Attach to stderr of the exec command.

            ConsoleSize	
                Array of integers or null = 2 items
                Initial console size, as an [height, width] array.

            DetachKeys	
                string
                    Override the key sequence for detaching a container. Format is a single character [a-Z] or ctrl-<value> where <value> is one of: a-z, @, ^, [, , or _.

            Tty	
                boolean
                    Allocate a pseudo-TTY.

            Env	
                Array of strings
                    A list of environment variables in the form ["VAR=value", ...].

            Cmd	
                Array of strings
                    Command to run, as a string or array of strings.

            Privileged	
                boolean
                    Default: false
                    Runs the exec process with extended privileges.

            User	
                string
                    The user, and optionally, group to run the exec process inside the container. Format is one of: user, user:group, uid, or uid:gid.

            WorkingDir	
                string
                    The working directory for the exec process inside the container.
        """
                
        return await self.containers.exec_run(container_id = container_id,params = params)
        
        
    async def start(self,instance_id,body :dict) -> dict:
        """
            Start an exec instance
                Starts a previously set up exec instance. If detach is true, this endpoint returns immediately after starting the command. Otherwise, it sets up an interactive session with the command.

            PATH PARAMETERS
                id
                    required
                        string
                            Exec instance ID

            REQUEST BODY SCHEMA: application/json
                Detach	
                    boolean
                        Detach from the command.

                Tty	
                    boolean
                        Allocate a pseudo-TTY.

                ConsoleSize	
                    Array of integers or null = 2 items
                        Initial console size, as an [height, width] array.
        """
        
        headers = {'Content-Type': 'application/json'}
        async with self.containers.session.post(f"{self.api_url}/exec/{instance_id}/start",headers=headers,json = body) as response:
            if response.status != 200 and response.status != 404 and response.status != 409 :
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker instance {instance_id}",
                    headers=response.headers
                )
            else:
                print(response)
                content_type = response.headers.get('Content-Type')
                if content_type in ['application/vnd.docker.multiplexed-stream','application/vnd.docker.raw-stream','application/json']:
                    async for chunk in response.content.iter_any():
                        try:
                            yield chunk.decode('utf-8', errors='ignore')
                        except UnicodeDecodeError:
                            yield chunk.decode(errors='replace')
                else:
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=f"Failed to response content_type {content_type} Docker container {container_id}",
                        headers=response.headers
                    )

        
    async def resize (self,instance_id:str,params: dict = None) -> dict:
        """
            Resize an exec instance
                Resize the TTY session used by an exec instance. This endpoint only works if tty was specified as part of creating and starting the exec instance.

            PATH PARAMETERS
                id
                    required
                        string
                        Exec instance ID

            QUERY PARAMETERS
                h	
                    integer
                        Height of the TTY session in characters

                w	
                    integer
                        Width of the TTY session in characters
        
        """
        
        async with self.containers.session.post(f"{self.api_url}/exec/{instance_id}/resize",params = params) as response:
            if response.status != 200 and response.status != 404 :
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker instance {instance_id}",
                    headers=response.headers
                )

            return await response.json()
        
    async def inspect(self,instance_id) -> dict:
        """
            Inspect an exec instance
                Return low-level information about an exec instance.

            PATH PARAMETERS
                id
                required
                    string
                        Exec instance ID
        """
        async with self.containers.session.get(f"{self.api_url}/exec/{instance_id}/json") as response:
            if response.status != 200 and response.status != 404:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
                    headers=response.headers
                )

            return await response.json()