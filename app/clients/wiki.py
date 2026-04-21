import asyncio

class WikiClient:
    def __init__(self, http, settings):
        self.http = http
        # Dynconf CONFIG
        self.base_url = settings.wiki.base_url

    # Base Request Method
    async def _request(self, method: str, title: str, **kwargs):

        url = self.base_url
        params = {
            "action": "parse",
            "format": "json",
            "prop": "text",
            "page": title,
        }
        headers = {
            'User-Agent': 'MediaWiki REST API docs examples/0.1 (https://www.mediawiki.org/wiki/API_talk:REST_API)'
        }
        response = await self.http.request(
            method,
            url,
            params=params,
            headers=headers,
            **kwargs
        )
        try:
            response.raise_for_status()
        except Exception as e:
            print(f"Wiki API error: {e}")
            print(await response.text())
            raise
        return response.json()

    async def get_title(self, title):
        return await self._request(
            "GET",
            f"{title}"
        )