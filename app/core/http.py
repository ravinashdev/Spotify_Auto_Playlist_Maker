# Cannot use httpx filename as python is recursively trying to import itself
import httpx
class HTTPClient:
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_connections=100)
        )

    # ** kwargs are preferred in case the method in not GET, POST, PUT, DELETE, example
    # Method for GET passing in **kwargs for params, payload and headers
    async def get(self, url, **kwargs):
        return await self.client.get(url, **kwargs)
    # Method for POST passing in **kwargs for params, payload and headers
    async def post(self, url, **kwargs):
        return await self.client.post(url, **kwargs)
    # Method for PUT passing in **kwargs for params, payload and headers
    async def put(self, url, **kwargs):
        return await self.client.put(url, **kwargs)
    # Method for DELETE passing in **kwargs for params, payload and headers
    async def delete(self, url, **kwargs):
        return await self.client.delete(url, **kwargs)
    # Method for close to terminate any open sockets or connections
    async def close(self):
        await self.client.aclose()