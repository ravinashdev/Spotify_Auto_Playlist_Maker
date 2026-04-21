import httpx
import logging

class HTTPClient:
    """
    Thin wrapper around httpx.AsyncClient.
    Purpose:
    - central configuration
    - optional logging hook
    - safe lifecycle management
    """
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            limits=httpx.Limits(max_connections=100),
        )
        self.logger = logging.getLogger(__name__)
# GENERIC REQUEST (BEST PRACTICE)
    async def request(self, method: str, url: str, **kwargs):
        # Single entry point for all HTTP calls.
        self.logger.debug(f"{method} {url}")
        response = await self.client.request(method, url, **kwargs)
        return response

    async def close(self):
        await self.client.aclose()