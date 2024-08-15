import asyncio
import aiohttp
import base64,json,os
import tarfile
from io import BytesIO
class Images:
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
                    Show all images. Only images from a final layer (no children) are shown by default.

            filters	
                string
                    A JSON encoded value of the filters (a map[string][]string) to process on the images list.

                    Available filters:

                        before=(<image-name>[:<tag>], <image id> or <image@digest>)
                        dangling=true
                        label=key or label="key=value" of an image label
                        reference=(<image-name>[:<tag>])
                        since=(<image-name>[:<tag>], <image id> or <image@digest>)
                        until=<timestamp>
            shared-size	
                boolean
                    Default: false
                    Compute and show shared size as a SharedSize field on each image.

            digests	
                boolean
                    Default: false
                    Show digest information as a RepoDigests field on each image.
        """
        async with self.session.get(f"{self.api_url}/images/json",params=params) as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Failed to query Docker image",
                    headers=response.headers
                )
            else:
                return await response.json()
        
    #to do
    async def build(self,x_registry_config :dict = None,params: dict = None,path = None):
        """
        QUERY PARAMETERS
        dockerfile	
            string
                Default: "Dockerfile"
                Path within the build context to the Dockerfile. This is ignored if remote is specified and points to an external Dockerfile.

        t	
            string
                A name and optional tag to apply to the image in the name:tag format. If you omit the tag the default latest value is assumed. You can provide several t parameters.

        extrahosts	
            string
                Extra hosts to add to /etc/hosts

        remote	
            string
                A Git repository URI or HTTP/HTTPS context URI. If the URI points to a single text file, the file’s contents are placed into a file called Dockerfile and the image is built from that file. If the URI points to a tarball, the file is downloaded by the daemon and the contents therein used as the context for the build. If the URI points to a tarball and the dockerfile parameter is also specified, there must be a file with the corresponding path inside the tarball.

        q	
            boolean
                Default: false
                Suppress verbose build output.

        nocache	
            boolean
                Default: false
                Do not use the cache when building the image.

        cachefrom	
            string
                JSON array of images used for build cache resolution.

        pull	
            string
                Attempt to pull the image even if an older image exists locally.

        rm	
            boolean
                Default: true
                Remove intermediate containers after a successful build.

        forcerm	
            boolean
                Default: false
                Always remove intermediate containers, even upon failure.

        memory	
            integer
                Set memory limit for build.

        memswap	
            integer
                Total memory (memory + swap). Set as -1 to disable swap.

        cpushares	
            integer
                CPU shares (relative weight).

        cpusetcpus	
            string
                CPUs in which to allow execution (e.g., 0-3, 0,1).

        cpuperiod	
            integer
                The length of a CPU period in microseconds.

        cpuquota	
            integer
                Microseconds of CPU time that the container can get in a CPU period.

        buildargs	
            string
                JSON map of string pairs for build-time variables. Users pass these values at build-time. Docker uses the buildargs as the environment context for commands run via the Dockerfile RUN instruction, or for variable expansion in other Dockerfile instructions. This is not meant for passing secret values.

                For example, the build arg FOO=bar would become {"FOO":"bar"} in JSON. This would result in the query parameter buildargs={"FOO":"bar"}. Note that {"FOO":"bar"} should be URI component encoded.

                Read more about the buildargs instruction.

        shmsize	
            integer
                Size of /dev/shm in bytes. The size must be greater than 0. If omitted the system uses 64MB.

        squash	
            boolean
                Squash the resulting images layers into a single layer. (Experimental release only.)

        labels	
            string
                Arbitrary key/value labels to set on the image, as a JSON map of string pairs.

        networkmode	
            string
                Sets the networking mode for the run commands during build. Supported standard values are: bridge, host, none, and container:<name|id>. Any other value is taken as a custom network's name or ID to which this container should connect to.

        platform	
            string
                Default: ""
                Platform in the format os[/arch[/variant]]

        target	
            string
                Default: ""
                Target build stage

        outputs	
            string
                Default: ""
                BuildKit output configuration

        version	
            string
                Default: "1"
                Enum: "1" "2"
            Version of the builder backend to use.

        1 is the first generation classic (deprecated) builder in the Docker daemon (default)
        2 is BuildKit
        
        HEADER PARAMETERS
            Content-type	
                string
                    Default: application/x-tar
                    Value: "application/x-tar"
            X-Registry-Config	
                string
                    This is a base64-encoded JSON object with auth configurations for multiple registries that a build may refer to.

            The key is a registry URL, and the value is an auth configuration object, as described in the authentication section. For example:

            {
            "docker.example.com": {
                "username": "janedoe",
                "password": "hunter2"
            },
            "https://index.docker.io/v1/": {
                "username": "mobydock",
                "password": "conta1n3rize14"
            }
            }
            Only the registry domain name (and port if not the default 443) are required. However, for legacy reasons, the Docker Hub registry must be specified with both a https:// prefix and a /v1/ suffix even though Docker will prefer to use the v2 registry API.

        REQUEST BODY SCHEMA: application/octet-stream
            A tar archive compressed with one of the following algorithms: identity (no compression), gzip, bzip2, xz.

            string <binary>
        """ 
        
        headers = {
            'Content-type':'application/x-tar',
            'X-Registry-Config': base64.b64encode(json.dumps(x_registry_config).encode('utf-8')).decode('utf-8')
        }
        
        tar_stream = BytesIO()
        with tarfile.open(fileobj=tar_stream, mode='w') as tar:
            tar.add(params['context_dir'], arcname=".")
        tar_stream.seek(0) 
        
        async with self.session.post(f"{self.api_url}/build",headers  = headers,params=params,data = tar_stream) as response:
            print(response)
            if response.status != 200:
                text = await response.text()
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker image {text}",
                    headers=response.headers
                )
                
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    async for chunk in response.content.iter_any():
                        try:
                            yield chunk.decode('utf-8', errors='ignore')
                        except UnicodeDecodeError:
                            yield chunk.decode(errors='replace')
                else:
                    yield response.text()     
    
        
    #to do
    async def build_prune(self,params: dict = None):
        """
        QUERY PARAMETERS
            keep-storage	
                integer <int64>
                    Amount of disk space in bytes to keep for cache

            all	
                boolean
                    Remove all types of build cache

            filters	
                string
                    A JSON encoded value of the filters (a map[string][]string) to process on the list of build cache objects.

            Available filters:

                until=<timestamp> remove cache older than <timestamp>. The <timestamp> can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g. 10m, 1h30m) computed relative to the daemon's local time.
                id=<id>
                parent=<id>
                type=<string>
                description=<string>
                inuse
                shared
                private
        """
        async with self.session.post(f"{self.api_url}/build/prune",params=params) as response:
            if response.status != 200 and response.status != 400:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to prune Docker image",
                    headers=response.headers
                )
            print(response)
            return await response.json()
        

    async def create(self,x_registry_auth :dict = None,identity_token:str = None,params: dict = None,body: dict = None):
        """
            Pull or import an image.

            QUERY PARAMETERS
                fromImage	
                    string
                        Name of the image to pull. The name may include a tag or digest. This parameter may only be used when pulling an image. The pull is cancelled if the HTTP connection is closed.

                fromSrc	
                    string
                        Source to import. The value may be a URL from which the image can be retrieved or - to read the image from the request body. This parameter may only be used when importing an image.

                repo	
                    string
                        Repository name given to an image when it is imported. The repo may include a tag. This parameter may only be used when importing an image.

                tag	
                    string
                        Tag or digest. If empty when pulling an image, this causes all tags for the given image to be pulled.

                message	
                    string
                        Set commit message for imported image.

                changes	
                    Array of strings
                        Apply Dockerfile instructions to the image that is created, for example: changes=ENV DEBUG=true. Note that ENV DEBUG=true should be URI component encoded.

                Supported Dockerfile instructions: CMD|ENTRYPOINT|ENV|EXPOSE|ONBUILD|USER|VOLUME|WORKDIR

                platform	
                    string
                        Default: ""
                        Platform in the format os[/arch[/variant]].

                When used in combination with the fromImage option, the daemon checks if the given image is present in the local image cache with the given OS and Architecture, and otherwise attempts to pull the image. If the option is not set, the host's native OS and Architecture are used. If the given image does not exist in the local image cache, the daemon attempts to pull the image with the host's native OS and Architecture. If the given image does exists in the local image cache, but its OS or architecture does not match, a warning is produced.

                When used with the fromSrc option to import an image from an archive, this option sets the platform information for the imported image. If the option is not set, the host's native OS and Architecture are used for the imported image.

            HEADER PARAMETERS
                X-Registry-Auth	
                    string
                        A base64url-encoded auth configuration.

                Refer to the authentication section for details.

            REQUEST BODY SCHEMA: 
                text/plain
                text/plain
                Image content if the value - has been specified in fromSrc query parameter string
        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """
        headers = {}
        if identity_token != None and identity_token != '':
            headers['identitytoken'] = identity_token

        if x_registry_auth != None:
            headers['X-Registry-Auth'] = base64.b64encode(json.dumps(x_registry_auth).encode('utf-8')).decode('utf-8')

        
        async with self.session.post(f"{self.api_url}/images/create",headers=headers,params=params) as response:
            if response.status != 200 and response.status != 404:
                print(response)
                text = await response.text()
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to create docker image {text}",
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
        
        
    async def inspect(self,image_name:str):
        """
            Inspect an image
                Return low-level information about an image.

            path Parameters
                name
                    required
                        string
                        Image name or id
        """
        

        async with self.session.get(f"{self.api_url}/images/{image_name}/json") as response:
            if response.status != 200 and response.status != 404:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker image {image_name}",
                    headers=response.headers
                )
            print(response)
            return await response.json()
        

    async def history (self,image_name:str):
        """
        Args:

            image_name
                required
                    string
                        Image name or ID
        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """

        async with self.session.get(f"{self.api_url}/images/{image_name}/history ") as response:
            if response.status != 200 and response.status != 404:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to query Docker image {image_name}",
                    headers=response.headers
                )

            else:
                print(response)
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()
        
        
        
        
    
    async def push(self,image_name:str,params: dict = None, identity_token:str = None,x_registry_auth :dict = None):
        """

            Push an image to a registry.

            If you wish to push an image on to a private registry, that image must already have a tag which references the registry. For example, registry.example.com/myimage:latest.

            The push is cancelled if the HTTP connection is closed.

            PATH PARAMETERS
                name
                required
                string
                Image name or ID.

            QUERY PARAMETERS
                tag	
                string
                The tag to associate with the image on the registry.

            HEADER PARAMETERS
                X-Registry-Auth
                required
                string
                A base64url-encoded auth configuration.

            Refer to the authentication section for details.
        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """
        headers = {}
        if identity_token != None and identity_token != '':
            headers['identitytoken'] = identity_token

        if x_registry_auth != None:
            headers['X-Registry-Auth'] = base64.b64encode(json.dumps(x_registry_auth).encode('utf-8')).decode('utf-8')


        async with self.session.post(f"{self.api_url}/images/{image_name}/push",headers = headers,params = params) as response:
            if response.status != 200 and response.status != 404:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to push docker image {image_name}",
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
        
    async def tag(self,image_name:str,params:dict = None):
        """
        Tag an image so that it becomes part of a repository.

            PATH PARAMETERS
                name
                    required
                        string
                            Image name or ID to tag.

            QUERY PARAMETERS
                repo	
                    string
                    The repository to tag in. For example, someuser/someimage.

                tag	
                    string
                    The name of the new tag.
        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """


        async with self.session.post(f"{self.api_url}/images/{image_name}/tag",params = params) as response:
            if response.status != 201 and response.status != 400 and response.status != 404 and response.status != 409:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to tag Docker image {image_name}",
                    headers=response.headers
                )
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()


    async def remove(self,image_name:str,params: dict = {"signal":"SIGINT","t":9}):
        """
        Remove an image, along with any untagged parent images that were referenced by that image.

        Images can't be removed if they have descendant images, are being used by a running container or are being used by a build.

        PATH PARAMETERS
            name
                required
                    string
                        Image name or ID

        QUERY PARAMETERS
            force	
                boolean
                    Default: false
                        Remove the image even if it is being used by stopped containers or has other tags

            noprune	
                boolean
                    Default: false
                        Do not delete untagged parent images
        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """


        async with self.session.delete(f"{self.api_url}/images/{image_name}",params = params) as response:
            if response.status != 200 and  response.status != 404 and  response.status != 409:
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to remove docker network {image_name}",
                    headers=response.headers
                )
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()
        
    async def search(self,params: dict = None):
        """
        Search images
        Search for an image on Docker Hub.

        QUERY PARAMETERS
        term
            required
            string
            Term to search

        limit	
            integer
            Maximum number of results to return

        filters	
            string
            A JSON encoded value of the filters (a map[string][]string) to process on the images list. Available filters:

            is-official=(true|false)
            stars=<number> Matches images that has at least 'number' stars.
        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """


        async with self.session.get(f"{self.api_url}/images/search",params = params) as response:
            if response.status != 200 and response.status != 400:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to search images",
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
        Delete unused images
        QUERY PARAMETERS
        filters	
        string
        Filters to process on the prune list, encoded as JSON (a map[string][]string). Available filters:

        dangling=<boolean> When set to true (or 1), prune only unused and untagged images. When set to false (or 0), all unused images are pruned.
        until=<string> Prune images created before this timestamp. The <timestamp> can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g. 10m, 1h30m) computed relative to the daemon machine’s time.
        label (label=<key>, label=<key>=<value>, label!=<key>, or label!=<key>=<value>) Prune images with (or without, in case label!=... is used) the specified labels.
        Responses
        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """


        async with self.session.post(f"{self.api_url}/images/prune",params = params) as response:
            if response.status != 200 :
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to delete unused images",
                    headers=response.headers
                )
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()


            
    async def commit(self,params: dict = None,data: dict = None):
        """
        QUERY PARAMETERS
        container	
        string
        The ID or name of the container to commit

        repo	
        string
        Repository name for the created image

        tag	
        string
        Tag name for the create image

        comment	
        string
        Commit message

        author	
        string
        Author of the image (e.g., John Hannibal Smith <hannibal@a-team.com>)

        pause	
        boolean
        Default: true
        Whether to pause the container before committing

        changes	
        string
        Dockerfile instructions to apply while committing

        REQUEST BODY SCHEMA: application/json
        The container configuration

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


        Raises:
            aiohttp.ClientResponseError: _description_

        Returns:
            _type_: _description_
        """

        headers = {'Content-Type':'application/json'}
        async with self.session.post(f"{self.api_url}/commit",headers=headers,params = params,data=data) as response:
            if response.status != 201 and response.status != 404 and response.status != 400:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to commit Docker image",
                    headers=response.headers
                )
            else:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/json':
                    return await response.json()
                else:
                    return await response.text()

        
    async def export(self,image_name:str,params: dict = None):
        """
        Export an image
        Get a tarball containing all images and metadata for a repository.

        If name is a specific name and tag (e.g. ubuntu:latest), then only that image (and its parents) are returned. If name is an image ID, similarly only that image (and its parents) are returned, but with the exclusion of the repositories file in the tarball, as there were no image names referenced.

        Image tarball format
        An image tarball contains one directory per image layer (named using its long ID), each containing these files:

        VERSION: currently 1.0 - the file format version
        json: detailed layer information, similar to docker inspect layer_id
        layer.tar: A tarfile containing the filesystem changes in this layer
        The layer.tar file contains aufs style .wh..wh.aufs files and directories for storing attribute changes and deletions.

        If the tarball defines a repository, the tarball should also include a repositories file at the root that contains a list of repository and tag names mapped to layer IDs.
                Raises:
            aiohttp.ClientResponseError: _description_
            
        PATH PARAMETERS
            name
                required
                    string
                        Image name or ID
                        
        QUERY PARAMETERS
            filename
                required
                    string
                        
            target_dir
                required
                    string
        Returns:
            _type_: _description_
        """

        inspect = await self.inspect(image_name = image_name)
        if "Id" in inspect:
            image_id = inspect['Id']
        else:
            return inspect
        
        async with self.session.get(f"{self.api_url}/images/{image_name}/get") as response:
            if response.status != 200 :
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed to export docker image {image_name}",
                    headers=response.headers
                )
            else:
                print(response)
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/x-tar':
                    if params != None:
                        filename = params.get('filename')
                        target_dir = params.get('target_dir','./')
                        if not os.path.exists(target_dir):
                            os.makedirs(target_dir)
                        if filename != None:
                            full_path = os.path.join(target_dir, filename)
                        else:
                            full_path = os.path.join(target_dir, image_id)     
                        
                    else:
                        full_path = os.path.join('./', image_id)
                        
                    with open(file = full_path + '.tar' ,mode = 'wb') as f:
                        while True:
                            chunk = await response.content.read(10240)
                            if not chunk:
                                break
                            f.write(chunk)
        return None


    async def exports (self,params:dict):
        """
        Export several images
        Get a tarball containing all images and metadata for several image repositories.

        For each value of the names parameter: if it is a specific name and tag (e.g. ubuntu:latest), then only that image (and its parents) are returned; if it is an image ID, similarly only that image (and its parents) are returned and there would be no names referenced in the 'repositories' file for this image ID.

        For details on the format, see the export image endpoint.

        QUERY PARAMETERS
            names	
                Array of strings
                    Image names to filter by
            filename
                string
            target_dir
                string

        Returns:
            _type_: _description_
        """
        
        if params != None:
            if params.get('filename') != None:
                async with self.session.get(f"{self.api_url}/images/get",params = {"names": params['names']}) as response:
                    if response.status != 200 :
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message=f"Failed to exports Docker image",
                            headers=response.headers
                        )
                    else:
                        content_type = response.headers.get('Content-Type')
                        if content_type == 'application/x-tar':
                            filename = params.get('filename')
                            target_dir = params.get('target_dir','./')
                            if not os.path.exists(target_dir):
                                os.makedirs(target_dir)
                            full_path = os.path.join(target_dir, filename)    
                
                            with open(file = full_path + '.tar' ,mode = 'wb') as f:
                                while True:
                                    chunk = await response.content.read(10240)
                                    if not chunk:
                                        break
                                    f.write(chunk)
        return None
          
        
        
    async def load (self,params: dict = None):
        """
        Import images
            Load a set of images and tags into a repository.

            For details on the format, see the export image endpoint.

            QUERY PARAMETERS
                quiet	
                    boolean
                        Default: false
                            Suppress progress details during load.
                filename
                    required
                        string
                        
                from_dir
                    required
                        string

            REQUEST BODY SCHEMA: application/x-tar
            Tar archive containing images

            string <binary>
            Responses


        Returns:
            _type_: _description_
        """
        headers = {'Content-Type':'application/x-tar'}
        tar_path = os.path.join(params['from_dir'], params['filename'])
    
        print(f"Attempting to open file at: {tar_path}")
        
        if not os.path.exists(tar_path):
            raise FileNotFoundError(f"File not found: {tar_path}")
        with open(tar_path, 'rb') as f:
            async with self.session.post(f"{self.api_url}/images/load",headers=headers,data=f) as response:
                if response.status != 200 :
                    print(response)
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=f"Failed to load Docker image",
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
        
# async def main():
#     containers = Containers("172.16.80.42","2376")
#     try:
#         ret = await containers.list(params = {"all":"true"})
#         print(ret)
#         print("*"*200)
#         ret = await containers.inspect(container_id = 'abe328cd52f33225e98b21700f379e5e6a71a953af2e4e7cb1727427bc187ecc')
#         print(ret)
#         print("*"*200)
#         ret = await containers.ps(container_id = 'abe328cd52f33225e98b21700f379e5e6a71a953af2e4e7cb1727427bc187ecc')
#         print(ret)
#         ret = await containers.top(container_id = 'abe328cd52f33225e98b21700f379e5e6a71a953af2e4e7cb1727427bc187ecc')
#         print(ret)
#         print("*"*200)
#         ret = await containers.changes(container_id = 'abe328cd52f33225e98b21700f379e5e6a71a953af2e4e7cb1727427bc187ecc')
#         print(ret)
#         # print("*"*200)
#         # ret = await containers.export(container_id = 'abe328cd52f33225e98b21700f379e5e6a71a953af2e4e7cb1727427bc187ecc')
#         # print(ret)
#         print("*"*200)
#         ret = await containers.stats(container_id = 'abe328cd52f33225e98b21700f379e5e6a71a953af2e4e7cb1727427bc187ecc')
#         print(ret)
        
#     finally:
#         await containers.close()

# # 运行异步主函数
# asyncio.run(main())
