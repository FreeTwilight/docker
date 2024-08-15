import asyncio
import aiohttp
import base64,json,os
import tarfile
from io import BytesIO


class Session:
    def __init__(self,hostname,port,interactive_session):       
        self.session = interactive_session
        self.hostname = hostname 
        self.port = port
        self.api_url = f"http://{self.hostname}:{self.port}"
        
        
    async def close(self):
        """
        关闭 ClientSession.
        """
        await self.session.close() 
        
    async def init_session(self) -> dict:
        """
        Initialize interactive session
            Start a new interactive session with a server. Session allows server to call back to the client for advanced capabilities.

            Hijacking
                This endpoint hijacks the HTTP connection to HTTP2 transport that allows the client to expose gPRC services on that connection.

                For example, the client sends this request to upgrade the connection:

                    POST /session HTTP/1.1
                    Upgrade: h2c
                    Connection: Upgrade
                The Docker daemon responds with a 101 UPGRADED response follow with the raw stream:

                    HTTP/1.1 101 UPGRADED
                    Connection: Upgrade
                    Upgrade: h2c
        """
        
        headers = {
            "Upgrade": "h2c",
            "Connection": "Upgrade",
        }

        async with self.session.post(f"{self.api_url}/session",headers = headers) as response:
            if response.status != 101  or response.headers.get("Upgrade", "").lower() != "h2c":
                print(response)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Failed Initialize interactive session!",
                    headers=response.headers
                )
            else:
                print(response)
                return await response.text()
        
