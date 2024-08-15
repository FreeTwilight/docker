import asyncio
import aiohttp
import json

class Containers:
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
    
    async def list(self,params: dict = None) -> dict:
        """
        QUERY PARAMETERS
            all	
                boolean
                Default: false
                Return all containers. By default, only running containers are shown.

            limit	
                integer
                Return this number of most recently created containers, including non-running ones.

            size	
                boolean
                Default: false
                Return the size of container as fields SizeRw and SizeRootFs.

            filters	
                string
                Filters to process on the container list, encoded as JSON (a map[string][]string). For example, {"status": ["paused"]} will only return paused containers.

                Available filters:

                    ancestor=(<image-name>[:<tag>], <image id>, or <image@digest>)
                    before=(<container id> or <container name>)
                    expose=(<port>[/<proto>]|<startport-endport>/[<proto>])
                    exited=<int> containers with exit code of <int>
                    health=(starting|healthy|unhealthy|none)
                    id=<ID> a container's ID
                    isolation=(default|process|hyperv) (Windows daemon only)
                    is-task=(true|false)
                    label=key or label="key=value" of a container label
                    name=<name> a container's name
                    network=(<network id> or <network name>)
                    publish=(<port>[/<proto>]|<startport-endport>/[<proto>])
                    since=(<container id> or <container name>)
                    status=(created|restarting|running|removing|paused|exited|dead)
                    volume=(<volume name> or <mount point destination>)
        """
        async with self.session.get(f"{self.api_url}/containers/json",params=params) as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Failed to query Docker container",
                    headers=response.headers
                )
            return await response.json()


        

    async def inspect(self,container_id:str,params: dict = None):
        """
        QUERY PARAMETERS
            size	
                boolean
                Default: false
                Return the size of container as fields SizeRw and SizeRootFs
        """ 
        async with self.session.get(f"{self.api_url}/containers/{container_id}/json",params=params) as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
                    headers=response.headers
                )
            return await response.json()
        
        

    async def top(self,container_id:str,params: dict = None):
        """
        QUERY PARAMETERS
            ps_args	
                string
                    Default: "-ef"
                    The arguments to pass to ps. For example, aux
        """
        async with self.session.get(f"{self.api_url}/containers/{container_id}/top",params=params) as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
                    headers=response.headers
                )
            return await response.json()
        
    async def ps(self,container_id:str,params: dict = None):
       return await self.top(container_id =container_id,params = params)
   
   
    
    async def logs(self,container_id:str,params: dict = {"stdout": True, "stderr": True}):
        """
        Args:
            container_id (str): _description_
            params (dict, optional): _description_. Defaults to None.
                QUERY PARAMETERS
                    follow	
                        boolean
                        Default: false
                        Keep connection after returning logs.

                stdout	
                    boolean
                        Default: false
                        Return logs from stdout

                stderr	
                    boolean
                        Default: false
                        Return logs from stderr

                since	
                    integer
                        Default: 0
                        Only return logs since this time, as a UNIX timestamp

                until	
                    integer
                        Default: 0
                        Only return logs before this time, as a UNIX timestamp

                timestamps	
                    boolean
                        Default: false
                        Add timestamps to every log line

                tail	
                    string
                        Default: "all"
                        Only return this number of log lines from the end of the logs. Specify as an integer or all to output all log lines.
        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """
        if params != None:
            params = {k: ('true' if v is True else 'false' if v is False else v) for k, v in params.items()}
        
        async with self.session.get(f"{self.api_url}/containers/{container_id}/logs",params=params) as response:
            if response.status != 200:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
                    headers=response.headers
                )
            else:
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

        
        
        
    async def changes(self,container_id:str):
        """
        Args:
            Returns which files in a container's filesystem have been added, deleted, or modified. The Kind of modification can be one of:

            0: Modified ("C")
            1: Added ("A")
            2: Deleted ("D")
        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """
        

        async with self.session.get(f"{self.api_url}/containers/{container_id}/changes") as response:
            if response.status != 200:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
                    headers=response.headers
                )

            return await response.json()
        
    #存在问题
    async def export(self,container_id:str):
        """
        Args:
            Export the contents of a container as a tarball.


        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """
        headers = {
            "Content-Type":"application/octet-stream"
        }

                
        async with self.session.get(f"{self.api_url}/containers/{container_id}/export", headers=headers) as response:
            if response.status != 200:        
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
                    headers=response.headers
                )

            else:
                import tqdm
                total_size = int(response.headers.get('Content-Length', 0))
                progress_bar = tqdm.tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024)
                with open(f"{container_id}.tar", "wb") as f:
                    async for data in response.content.iter_chunked(1024):
                        f.write(data)
                        progress_bar.update(len(data))
                progress_bar.close()
                print(f"Container {container_id} exported successfully.")

                    

        
        
        
    
    async def stats(self,container_id:str,params: dict = {"stream":"true"}):
        """

        Export the contents of a container as a tarball.
        This endpoint returns a live stream of a container’s resource usage statistics.

        The precpu_stats is the CPU statistic of the previous read, and is used to calculate the CPU usage percentage. It is not an exact copy of the cpu_stats field.

        If either precpu_stats.online_cpus or cpu_stats.online_cpus is nil then for compatibility with older daemons the length of the corresponding cpu_usage.percpu_usage array should be used.

        On a cgroup v2 host, the following fields are not set

            blkio_stats: all fields other than io_service_bytes_recursive
            cpu_stats: cpu_usage.percpu_usage
            memory_stats: max_usage and failcnt Also, memory_stats.stats fields are incompatible with cgroup v1.
        To calculate the values shown by the stats command of the docker cli tool the following formulas can be used:

            used_memory = memory_stats.usage - memory_stats.stats.cache
            available_memory = memory_stats.limit
            Memory usage % = (used_memory / available_memory) * 100.0
            cpu_delta = cpu_stats.cpu_usage.total_usage - precpu_stats.cpu_usage.total_usage
            system_cpu_delta = cpu_stats.system_cpu_usage - precpu_stats.system_cpu_usage
            number_cpus = lenght(cpu_stats.cpu_usage.percpu_usage) or cpu_stats.online_cpus
            CPU usage % = (cpu_delta / system_cpu_delta) * number_cpus * 100.0
        
        Args:
            QUERY PARAMETERS
            stream	
                boolean
                    Default: true
                    Stream the output. If false, the stats will be output once and then it will disconnect.

            one-shot	
                boolean
                    Default: false
                    Only get a single stat instead of waiting for 2 cycles. Must be used with stream=false.
        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """


        async with self.session.get(f"{self.api_url}/containers/{container_id}/stats",params = params) as response:
            if response.status != 200:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
                    headers=response.headers
                )
                
            if params.get("stream", "true") == "true":
                async for line in response.content:
                    yield json.loads(line.decode('utf-8'))
            else:
                yield await response.json()


        



    async def create(self,params: dict = None,body : dict = None):
        """
        
        name	
            string^/?[a-zA-Z0-9][a-zA-Z0-9_.-]+$
                Assign the specified name to the container. Must match /?[a-zA-Z0-9][a-zA-Z0-9_.-]+.

        platform	
            string
                Default: ""
                Platform in the format os[/arch[/variant]] used for image lookup.

        When specified, the daemon checks if the requested image is present in the local image cache with the given OS and Architecture, and otherwise returns a 404 status.

        If the option is not set, the host's native OS and Architecture are used to look up the image in the image cache. However, if no platform is passed and the given image does exist in the local image cache, but its OS or architecture does not match, the container is created with the available image, and a warning is added to the Warnings field in the response, for example;

        WARNING: The requested image's platform (linux/arm64/v8) does not
                match the detected host platform (linux/amd64) and no
                specific platform was requested
        
        REQUEST BODY SCHEMA: 
        required
            Container to create

            Hostname	
                string
                    The hostname to use for the container, as a valid RFC 1123 hostname.

            Domainname	
                string
                    The domain name to use for the container.

            User	
                string
                    The user that commands are run as inside the container.

            AttachStdin	
                boolean
                    Default: false
                        Whether to attach to stdin.

            AttachStdout	
                boolean
                    Default: true
                        Whether to attach to stdout.

            AttachStderr	
                boolean
                    Default: true
                        Whether to attach to stderr.

            ExposedPorts	
                object or null
                        An object mapping ports to an empty object in the form:

            {"<port>/<tcp|udp|sctp>": {}}

            Tty	
            boolean
                Default: false
                    Attach standard streams to a TTY, including stdin if it is not closed.

            OpenStdin	
                boolean
                    Default: false
                        Open stdin

            StdinOnce	
                boolean
                    Default: false
                        Close stdin after one attached client disconnects

            Env	
                Array of strings
                    A list of environment variables to set inside the container in the form ["VAR=value", ...]. A variable without = is removed from the environment, rather than to have an empty value.

            Cmd	
                Array of strings
                    Command to run specified as a string or an array of strings.

            Healthcheck	
                object (HealthConfig)
                    A test to perform to check that the container is healthy.

            ArgsEscaped	
                boolean or null
                    Default: false
                        Command is already escaped (Windows only)

            Image	
                string
                    The name (or reference) of the image to use when creating the container, or which was used when the container was created.

            Volumes	
                object
                    An object mapping mount point paths inside the container to empty objects.

            WorkingDir	
                string
                    The working directory for commands to run in.

            Entrypoint	
                Array of strings
                    The entry point for the container as a string or an array of strings.

                    If the array consists of exactly one empty string ([""]) then the entry point is reset to system default (i.e., the entry point used by docker when there is no ENTRYPOINT instruction in the Dockerfile).

            NetworkDisabled	
                boolean or null
                    Disable networking for the container.

            MacAddress	
                string or null
                    MAC address of the container.

                Deprecated: this field is deprecated in API v1.44 and up. Use EndpointSettings.MacAddress instead.

            OnBuild	
                Array of strings or null
                    ONBUILD metadata that were defined in the image's Dockerfile.

            Labels	
                object
                    User-defined key/value metadata.

            StopSignal	
                string or null
                    Signal to stop a container as a string or unsigned integer.

            StopTimeout	
                integer or null
                    Default: 10
                    Timeout to stop a container in seconds.

            Shell	
                Array of strings or null
                    Shell for when RUN, CMD, and ENTRYPOINT uses a shell.

            HostConfig	
                object (HostConfig)
                    Container configuration that depends on the host we are running on

            NetworkingConfig	
                object (NetworkingConfig)
                    NetworkingConfig represents the container's networking configuration for each of its interfaces. It is used for the networking configs specified in the docker create and docker network connect commands.
        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """

        headers = {'Content-Type': 'application/json'}
        async with self.session.post(f"{self.api_url}/containers/create", headers=headers,params = params, json = body) as response:
            if response.status != 201 and response.status != 409 and response.status != 404 :
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=response.text(),
                    headers=response.headers
                )
            return await response.json(),response.status

    async def run(self,params: dict = None,body:dict = None,detachKeys:str = ' ctrl-z'):
        container_information,status = await self.create(params = params,body =body)
        if status != 201:
            return container_information
        else:
            return await self.start(container_information['Id'] , params = {'detachKeys':detachKeys})
        
    async def stop(self,container_id:str,params: dict = {"signal":"SIGINT","t":2}):
        """
        QUERY PARAMETERS
        signal	
            string
              Signal to send to the container as an integer or string (e.g. SIGINT).

        t	
            integer
                Number of seconds to wait before killing the container
        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """


        async with self.session.post(f"{self.api_url}/containers/{container_id}/stop",params = params) as response:
            if response.status != 204 and response.status != 304:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
                    headers=response.headers
                )
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()
        
    async def kill(self,container_id:str,params: dict = {"signal":"SIGINT","t":9}):
        """
        QUERY PARAMETERS
            signal	
                string
                    Default: "SIGKILL"
                    Signal to send to the container as an integer or string (e.g. SIGINT).
        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """


        async with self.session.post(f"{self.api_url}/containers/{container_id}/kill",params = params) as response:
            if response.status != 204 and response.status != 404 and  response.status != 409:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
                    headers=response.headers
                )

            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()

        
    async def wait(self,container_id:str,params: dict = None):
        """
        QUERY PARAMETERS
                condition	
                    string
                        Default: "not-running"
                        Enum: "not-running" "next-exit" "removed"
                        Wait until a container state reaches the given condition.

                        Defaults to not-running if omitted or empty.
        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """


        async with self.session.post(f"{self.api_url}/containers/{container_id}/wait",params = params) as response:
            if response.status != 200 :
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
                    headers=response.headers
                )

            return await response.json()
        
    async def remove(self,container_id:str,params: dict = None):
        """
        QUERY PARAMETERS
                v	
                boolean
                Default: false
                Remove anonymous volumes associated with the container.

                force	
                boolean
                Default: false
                If the container is running, kill it before removing it.

                link	
                boolean
                Default: false
                Remove the specified link associated with the container.


        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """


        async with self.session.delete(f"{self.api_url}/containers/{container_id}",params = params) as response:
            if response.status != 204 :
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
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

                        until=<timestamp> Prune containers created before this timestamp. The <timestamp> can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g. 10m, 1h30m) computed relative to the daemon machine’s time.
                        label (label=<key>, label=<key>=<value>, label!=<key>, or label!=<key>=<value>) Prune containers with (or without, in case label!=... is used) the specified labels.

        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """

        async with self.session.post(f"{self.api_url}/containers/prune",params = params) as response:
            if response.status != 200 :
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container",
                    headers=response.headers
                )

            return await response.json()        
        

    
    async def attach(self,container_id:str,params: dict = None):
        """
        PATH PARAMETERS
            id
                required
                    string
                        ID or name of the container

        QUERY PARAMETERS
            detachKeys	
                string
                    Override the key sequence for detaching a container.Format is a single character [a-Z] or ctrl-<value> where <value> is one of: a-z, @, ^, [, , or _.

            logs	
                boolean
                    Default: false
                        Replay previous logs from the container.
                        This is useful for attaching to a container that has started and you want to output everything since the container started.
                        If stream is also enabled, once all the previous output has been returned, it will seamlessly transition into streaming current output.

            stream	
                boolean
                    Default: false
                        Stream attached streams from the time the request was made onwards.

            stdin	
                boolean
                    Default: false
                        Attach to stdin

            stdout	
                boolean
                    Default: false
                        Attach to stdout

            stderr	
                boolean
                    Default: false
                        Attach to stderr
        """

        async with self.session.post(f"{self.api_url}/containers/{container_id}/attach",params = params) as response:
            if response.status != 200 and response.status != 101 and response.status != 400 and response.status != 404:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
                    headers=response.headers
                )
            content_type = response.headers.get('Content-Type')
            if content_type == 'application/json':
                return await response.json()
            else:
                return await response.text()
                 
    async def attach_socket(self,container_id:str,params: dict = None):
        """
        PATH PARAMETERS
            id
                required
                    string
                        ID or name of the container

        QUERY PARAMETERS
            detachKeys	
                string
                    Override the key sequence for detaching a container.Format is a single character [a-Z] or ctrl-<value> where <value> is one of: a-z, @, ^, [, ,, or _.

            logs	
                boolean
                    Default: false
                        Return logs

            stream	
                boolean
                    Default: false
                        Return stream

            stdin	
                boolean
                    Default: false
                        Attach to stdin

            stdout	
                boolean
                    Default: false
                        Attach to stdout

            stderr	
                boolean
                    Default: false
                        Attach to stderr
        """

        async with self.session.get(f"{self.api_url}/containers/{container_id}/attach/ws",params = params) as response:
            if response.status != 200 and response.status != 101 and response.status != 404 and response.status != 400:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
                    headers=response.headers
                )
            content_type = response.headers.get('Content-Type')
            if content_type == 'application/json':
                return await response.json()
            else:
                return await response.text()      
        
        
    async def exec_run(self,container_id:str,body: dict = None):
        """
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
        headers = {'Content-Type': 'application/json'}
        async with self.session.post(f"{self.api_url}/containers/{container_id}/exec",json = params,headers=headers) as response:
            if response.status != 201 and response.status != 404 and response.status != 409 :
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
                    headers=response.headers
                )

            return await response.json()
           
    async def get_archive(self,container_id:str,params: dict = None):
        """
        Get a tar archive of a resource in the filesystem of container id.

        PATH PARAMETERS
            id
                required
                    string
                        ID or name of the container

        QUERY PARAMETERS
            path
                required
                    string
                        Resource in the container’s filesystem to archive.
        """

        async with self.session.get(f"{self.api_url}/containers/{container_id}/archive",params = params) as response:
            if response.status != 200 and response.status != 400 and response.status != 404:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
                    headers=response.headers
                )
            content_type = response.headers.get('Content-Type')
            if content_type == 'application/json':
                return await response.json()
            else:
                return await response.text()   
        
   
    async def put_archive(self,container_id:str,params: dict = None):
        """
        Upload a tar archive to be extracted to a path in the filesystem of container id. path parameter is asserted to be a directory. If it exists as a file, 400 error will be returned with message "not a directory".

        PATH PARAMETERS
            id
                required
                    string
                        ID or name of the container

        QUERY PARAMETERS
            path
                required
                    string
                        Path to a directory in the container to extract the archive’s contents into.

            noOverwriteDirNonDir	
                string
                    If 1, true, or True then it will be an error if unpacking the given content would cause an existing directory to be replaced with a non-directory and vice versa.

            copyUIDGID	
                string
                    If 1, true, then it will copy UID/GID maps to the dest file or dir

        REQUEST BODY SCHEMA: 
            application/x-tar
            application/x-tar
            required
            The input stream must be a tar archive compressed with one of the following algorithms: identity (no compression), gzip, bzip2, or xz.

            string <binary>
        """

        async with self.session.put(f"{self.api_url}/containers/{container_id}/archive",params = params) as response:
            if response.status != 200 :
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
                    headers=response.headers
                )

            return await response.json()
        
    async def rename(self,container_id:str,params: dict = None):
        """
        PATH PARAMETERS
            id
                required
                    string
                        ID or name of the container

        QUERY PARAMETERS
            name
                required
                    string
                        New name for the container
        """

        async with self.session.post(f"{self.api_url}/containers/{container_id}/rename",params = params) as response:
            if response.status != 204 and response.status != 404 and response.status != 400 :
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to rename Docker container {container_id}",
                    headers=response.headers
                )
            content_type = response.headers.get('Content-Type')
            if content_type == 'application/json':
                return await response.json()
            else:
                return await response.text()
           
    async def resize(self,container_id:str,params: dict = None):
        """
        Resize the TTY for a container.

        PATH PARAMETERS
            id
                required
                    string
                        ID or name of the container

        QUERY PARAMETERS
            h	
                integer
                    Height of the TTY session in characters

            w	
                integer
                    Width of the TTY session in characters
        """

        async with self.session.post(f"{self.api_url}/containers/{container_id}/resize",params = params) as response:
            if response.status != 200 and response.status != 404:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
                    headers=response.headers
                )
            content_type = response.headers.get('Content-Type')
            if content_type == 'application/json':
                return await response.json()
            else:
                return await response.text()
        
        
    async def restart(self,container_id:str,params: dict = None):
        """
        PATH PARAMETERS
            id
                required
                string
                ID or name of the container

        QUERY PARAMETERS
            signal	
                string
                Signal to send to the container as an integer or string (e.g. SIGINT).
        t	
            integer
                Number of seconds to wait before killing the container
        """

        async with self.session.post(f"{self.api_url}/containers/{container_id}/restart",params = params) as response:
            if response.status != 204 and response.status != 404:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to restart Docker container {container_id}",
                    headers=response.headers
                )
            content_type = response.headers.get('Content-Type')
            if content_type == 'application/json':
                return await response.json()
            else:
                return await response.text()
        
        
    async def start(self,container_id:str,params: dict = None):
        """

            id
                required
                    string
                        ID or name of the container

            query Parameters
                detachKeys	
                    string
                        Override the key sequence for detaching a container. Format is a single character [a-Z] or ctrl-<value> where <value> is one of: a-z, @, ^, [, , or _.
        """

        async with self.session.post(f"{self.api_url}/containers/{container_id}/start",params = params) as response:
            if response.status != 204 and   response.status != 304 and response.status != 404 :
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker container {container_id}",
                    headers=response.headers
                )
            content_type = response.headers.get('Content-Type')
            if content_type == 'application/json':
                return await response.json()
            else:
                return await response.text()
        
    async def pause(self,container_id:str,params: dict = None):
        """
        Use the freezer cgroup to suspend all processes in a container.

        Traditionally, when suspending a process the SIGSTOP signal is used, which is observable by the process being suspended. With the freezer cgroup the process is unaware, and unable to capture, that it is being suspended, and subsequently resumed.

        PATH PARAMETERS
            id
                required
                    string
                        ID or name of the container
        """

        async with self.session.post(f"{self.api_url}/containers/{container_id}/pause",params = params) as response:
            if response.status != 204 and response.status != 404:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to pause Docker container {container_id}",
                    headers=response.headers
                )
            content_type = response.headers.get('Content-Type')
            if content_type == 'application/json':
                return await response.json()
            else:
                return await response.text()
    
    async def unpause(self,container_id:str,params: dict = None):
        """
        Resume a container which has been paused.

        PATH PARAMETERS
            id
                required
                    string
                        ID or name of the container
        """

        async with self.session.post(f"{self.api_url}/containers/{container_id}/unpause",params = params) as response:
            if response.status != 204 and  response.status != 404:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to unpause Docker container {container_id}",
                    headers=response.headers
                )
            content_type = response.headers.get('Content-Type')
            if content_type == 'application/json':
                return await response.json()
            else:
                return await response.text()
        
    async def update(self,container_id:str,body: dict = None):
        """
        Change various configuration options of a container without having to recreate it.

        PATH PARAMETERS
            id
            required
            string
            ID or name of the container

        REQUEST BODY SCHEMA: application/json
            required
            CpuShares	
            integer
            An integer value representing this container's relative CPU weight versus other containers.

            Memory	
            integer <int64>
            Default: 0
            Memory limit in bytes.

            CgroupParent	
            string
            Path to cgroups under which the container's cgroup is created. If the path is not absolute, the path is considered to be relative to the cgroups path of the init process. Cgroups are created if they do not already exist.

            BlkioWeight	
            integer [ 0 .. 1000 ]
            Block IO weight (relative weight).

            BlkioWeightDevice	
            Array of objects
            Block IO weight (relative device weight) in the form:

            [{"Path": "device_path", "Weight": weight}]
            BlkioDeviceReadBps	
            Array of objects (ThrottleDevice)
            Limit read rate (bytes per second) from a device, in the form:

            [{"Path": "device_path", "Rate": rate}]
            BlkioDeviceWriteBps	
            Array of objects (ThrottleDevice)
            Limit write rate (bytes per second) to a device, in the form:

            [{"Path": "device_path", "Rate": rate}]
            BlkioDeviceReadIOps	
            Array of objects (ThrottleDevice)
            Limit read rate (IO per second) from a device, in the form:

            [{"Path": "device_path", "Rate": rate}]
            BlkioDeviceWriteIOps	
            Array of objects (ThrottleDevice)
            Limit write rate (IO per second) to a device, in the form:

            [{"Path": "device_path", "Rate": rate}]
            CpuPeriod	
            integer <int64>
            The length of a CPU period in microseconds.

            CpuQuota	
            integer <int64>
            Microseconds of CPU time that the container can get in a CPU period.

            CpuRealtimePeriod	
            integer <int64>
            The length of a CPU real-time period in microseconds. Set to 0 to allocate no time allocated to real-time tasks.

            CpuRealtimeRuntime	
            integer <int64>
            The length of a CPU real-time runtime in microseconds. Set to 0 to allocate no time allocated to real-time tasks.

            CpusetCpus	
            string
            CPUs in which to allow execution (e.g., 0-3, 0,1).

            CpusetMems	
            string
            Memory nodes (MEMs) in which to allow execution (0-3, 0,1). Only effective on NUMA systems.

            Devices	
            Array of objects (DeviceMapping)
            A list of devices to add to the container.

            DeviceCgroupRules	
            Array of strings
            a list of cgroup rules to apply to the container

            DeviceRequests	
            Array of objects (DeviceRequest)
            A list of requests for devices to be sent to device drivers.

            KernelMemoryTCP	
            integer <int64>
            Hard limit for kernel TCP buffer memory (in bytes). Depending on the OCI runtime in use, this option may be ignored. It is no longer supported by the default (runc) runtime.

            This field is omitted when empty.

            MemoryReservation	
            integer <int64>
            Memory soft limit in bytes.

            MemorySwap	
            integer <int64>
            Total memory limit (memory + swap). Set as -1 to enable unlimited swap.

            MemorySwappiness	
            integer <int64> [ 0 .. 100 ]
            Tune a container's memory swappiness behavior. Accepts an integer between 0 and 100.

            NanoCpus	
            integer <int64>
            CPU quota in units of 10-9 CPUs.

            OomKillDisable	
            boolean
            Disable OOM Killer for the container.

            Init	
            boolean or null
            Run an init inside the container that forwards signals and reaps processes. This field is omitted if empty, and the default (as configured on the daemon) is used.

            PidsLimit	
            integer or null <int64>
            Tune a container's PIDs limit. Set 0 or -1 for unlimited, or null to not change.

            Ulimits	
            Array of objects
            A list of resource limits to set in the container. For example:

            {"Name": "nofile", "Soft": 1024, "Hard": 2048}
            CpuCount	
            integer <int64>
            The number of usable CPUs (Windows only).

            On Windows Server containers, the processor resource controls are mutually exclusive. The order of precedence is CPUCount first, then CPUShares, and CPUPercent last.

            CpuPercent	
            integer <int64>
            The usable percentage of the available CPUs (Windows only).

            On Windows Server containers, the processor resource controls are mutually exclusive. The order of precedence is CPUCount first, then CPUShares, and CPUPercent last.

            IOMaximumIOps	
            integer <int64>
            Maximum IOps for the container system drive (Windows only)

            IOMaximumBandwidth	
            integer <int64>
            Maximum IO in bytes per second for the container system drive (Windows only).

            RestartPolicy	
            object (RestartPolicy)
            The behavior to apply when the container exits. The default is not to restart.

            An ever increasing delay (double the previous delay, starting at 100ms) is added before each restart to prevent flooding the server.
        """

        async with self.session.post(f"{self.api_url}/containers/{container_id}/update",json = body) as response:
            if response.status != 200 and response.status != 404 and response.status != 400:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to update Docker container {container_id}",
                    headers=response.headers
                )
            content_type = response.headers.get('Content-Type')
            if content_type == 'application/json':
                return await response.json()
            else:
                return await response.text()        





