import httpx

class HTTPClient:
    # Thin wrapper around httpx.AsyncClient.
    # Purpose:
    # - central configuration
    # - safe lifecycle management
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            limits=httpx.Limits(max_connections=100),
        )

    # Generic Request
    async def request(self, method: str, url: str, **kwargs):
        # Single entry point for all HTTP calls.
        response = await self.client.request(method, url, **kwargs)
        return response
    # Close to free up network connections and resources
    async def close(self):
        await self.client.aclose()