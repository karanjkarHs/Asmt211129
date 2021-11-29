###################################################################
#Script Name	: httpClient                                                                                             
#Description	: Asychronous client to proess http request.                                                                                                                                                                          
#Author       	: Harshad S Karanjkar                                                
#Date         	: Jul 2021
#Last Modified  :
#Modified By    :                                             
###################################################################
#get home directory path
from sys import path
from pathlib import Path
path.append(str(Path(__file__).resolve().parent.parent))
from os import system
from shared.log import logger
import aiohttp
import asyncio
import collections
import json
from aiohttp import TCPConnector

class HttpClient:
    """ Asychronous client to proess http request"""
    def __init__(self, method, url, headers, payload, timeout):
        self.method = method.lower()
        self.url = url
        self.timeout = timeout
        self.payload = json.dumps(payload)
        self.headers = headers

    @logger.catch
    async def main(self):

        # Retrieve resource representation
        if self.method == 'get':
            try:

                logger.info(f'[ayncApiRequest.get] get request to url: {self.url}')
                async with aiohttp.ClientSession(conn_timeout=self.timeout, connector=TCPConnector(verify_ssl=False)) as session:
                    async with session.get(self.url,
                                           headers=self.headers
                                            ) as response:
                        status = response.status   
                        contentType = response.headers['content-type']
                        data = await response.text()
                        logger.info(f'[ayncApiRequest.get] Get request returned with status: {status}')
                        return data, status, contentType

            except Exception as error:
                logger.info(f'[ayncApiRequest.get] Get request failed: {error}')
                logger.error(f'[ayncApiRequest.get] Get request failed: {error}')
                return

        # Create new subordinate resources
        if self.method == 'post':
            try:

                logger.info(f'[ayncApiRequest.post] post request to url: {self.url}')
                async with aiohttp.ClientSession(conn_timeout=self.timeout, connector=TCPConnector(verify_ssl=False)) as session:
                    async with session.post(self.url,
                                            headers=self.headers, 
                                            data=self.payload
                                            ) as response:
                        status = response.status   
                        contentType = response.headers['content-type']   
                        data = await response.text()
                        logger.info(f'[ayncApiRequest.post] post request returned with status: {status}')
                        return data, status, contentType

            except Exception as error:
                logger.info(f'[ayncApiRequest.post] post request failed: {error}')
                logger.error(f'[ayncApiRequest.post] post request failed: {error}')
                return

        # Update existing resource
        if self.method == 'put':
            try:

                logger.info(f'[ayncApiRequest.put] put request to url: {self.url}')
                async with aiohttp.ClientSession(conn_timeout=self.timeout, connector=TCPConnector(verify_ssl=False)) as session:
                    async with session.put(self.url,
                                           headers=self.headers, 
                                           data=self.payload        
                                           ) as response:
                        status = response.status   
                        contentType = response.headers['content-type']   
                        data = await response.text()
                        logger.info(f'[ayncApiRequest.put] put request returned with status: {status}')
                        return data, status, contentType

            except Exception as error:
                logger.info(f'[ayncApiRequest.put] put request failed: {error}')
                logger.error(f'[ayncApiRequest.put] put request failed: {error}')
                return

        # Delete resources
        if self.method == 'delete':
            try:

                logger.info(f'[ayncApiRequest.delete] delete request to url: {self.url}')
                async with aiohttp.ClientSession(conn_timeout=self.timeout, connector=TCPConnector(verify_ssl=False)) as session:
                    async with session.delete(self.url,
                                              headers=self.headers
                                            ) as response:
                        status = response.status   
                        contentType = response.headers['content-type']   
                        data = await response.text()
                        logger.info(f'[ayncApiRequest.delete] delete request returned with status: {status}')
                        return data, status, contentType

            except Exception as error:
                logger.info(f'[ayncApiRequest.delete] delete request failed: {error}')
                logger.error(f'[ayncApiRequest.delete] delete request failed: {error}')
                return

        # Partial update on a resource
        if self.method == 'patch':
            try:

                logger.info(f'[ayncApiRequest.patch] patch request to url: {self.url}')
                async with aiohttp.ClientSession(conn_timeout=self.timeout, connector=TCPConnector(verify_ssl=False)) as session:
                    async with session.patch(self.url,
                                            headers=self.headers, 
                                            data=self.payload         
                                            ) as response:
                        status = response.status   
                        contentType = response.headers['content-type']   
                        data = await response.text()
                        logger.info(f'[ayncApiRequest.patch] patch request returned with status: {status}')
                        return data, status, contentType

            except Exception as error:
                logger.info(f'[ayncApiRequest.patch] patch request failed: {error}')
                logger.error(f'[ayncApiRequest.patch] patch request failed: {error}')
                return

@logger.catch
def httpClient(method, url, headers={}, payload={}, timeout=600):
    try:
        client = HttpClient(method, url, headers, payload, timeout)
        loop = asyncio.get_event_loop()
        data, status, contentType = loop.run_until_complete(client.main())
        result = collections.OrderedDict()
        result["status"] = status
        result["Content-type"] = contentType
        result["data"] = data
        result = json.dumps(result)
        #logger.info(f'[ayncApiRequest.requestHandler] Result: {result}')
        return result       
    except Exception as error:
        logger.info(f'[ayncApiRequest.requestHandler] Request failed: {error}')
        logger.error(f'[ayncApiRequest.requestHandler] Request failed: {error}')
        return 400


if __name__ =="__main__":
    try:    
        obj = HttpClient('post','http://python.org', payload={}, headers={'Authorization': 'Bearer authToken', 
                'Content-Type': 'application/json',
                'userId' : 'aditydu1@in.ibm.com'}, timeout=600)
        loop = asyncio.get_event_loop()
        data, status, contentType = loop.run_until_complete(obj.main())    
        result = collections.OrderedDict()
        result["status"] = status
        result["Content-type"] = contentType
        result["data"] = data[:15], "..."
        result = json.dumps(result)
        print(result)       
    except Exception as error:
        print(400)        