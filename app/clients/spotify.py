import base64
import time
import asyncio

class SpotifyClient:
    # Clean async API client for Spotify.
    # Responsibilities:
    # - Manage OAuth token lifecycle
    # - Cache token in memory
    # - Make authenticated API requests
    # - Provide clean endpoint methods
    # - Enforcing with Type to limit Bad API Requests
    def __init__(self, http, settings):
        self.http = http
        # Dynconf CONFIG
        self.base_url = settings.spotify.base_url
        self.request_access_token_url = settings.spotify.request_access_token_url
        self.client_id = settings.SPOTIFY_API_CLIENT_ID
        self.client_secret = settings.SPOTIFY_API_CLIENT_SECRET
        # Token Cache State
        self._access_token = None
        self._expires_at = 0
        self._lock = asyncio.Lock()

    # FETCH NEW TOKEN
    async def _fetch_access_token(self):
        creds = f"{self.client_id}:{self.client_secret}"
        encoded_creds = base64.b64encode(creds.encode()).decode()
        headers = {
            "Authorization": f"Basic {encoded_creds}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        payload = {
            "grant_type": "client_credentials",
        }
        response = await self.http.request(
            "POST",
            self.request_access_token_url,
            data=payload,
            headers=headers
        )
        response.raise_for_status()
        data = response.json()
        self._access_token = data["access_token"]
        self._expires_at = time.time() + data["expires_in"] - 60

    # GET TOKEN (WITH CACHE)
    async def get_access_token(self):
        # Check if access token is still valid in the cache based on time
        if self._access_token and time.time() < self._expires_at:
            return self._access_token
        # If it's not valid/expired we get/fetch a new one to limit requests
        async with self._lock:
            if self._access_token and time.time() < self._expires_at:
                return self._access_token
            await self._fetch_access_token()
            return self._access_token

    # BASE REQUEST METHOD
    async def _request(self, method: str, endpoint: str, **kwargs):
        token = await self.get_access_token()
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        url = f"{self.base_url}{endpoint}"
        response = await self.http.request(
            method,
            url,
            headers=headers,
            **kwargs
        )
        try:
            response.raise_for_status()
        except Exception as e:
            print(f"Spotify API error: {e}")
            print(await response.text())
            raise
        return response.json()

    # ENDPOINTS
    # 1.GET Artist
    async def get_artist(self, artist_id: str):
        return await self._request(
            "GET",
            f"/artists/{artist_id}"
        )
