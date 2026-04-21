# ---------------------------- IMPORTS ------------------------------- #
# Used to return a printed report for Dynaconf for debugging
# from dynaconf import inspect_settings
# inspect_settings(settings, print_report=True)
import asyncio
import json
from core.config import settings
from core.http import HTTPClient
# Import All Clients Classes
from clients.spotify import SpotifyClient

# ---------------------------- CONSTANTS ------------------------------- #
http = HTTPClient()
spotify = SpotifyClient(http, settings)
# ---------------------------- GLOBAL VARIABLES ------------------------------- #

# ---------------------------- FUNCTIONS ------------------------------- #
async def main():
    try:
        # Spotify API Series Calls
        spotify_get_artist_data_response = await spotify.get_artist(
            artist_id="0TnOYISbd1XYRBk9myaseg",
        )
        print(json.dumps(spotify_get_artist_data_response, indent=4))
        # Spotify API Parallel Calls
        # results = await asyncio.gather(
        #     spotify.get_artist("id1"),
        #     spotify.get_artist("id2"),
        #     spotify.get_artist("id3")
        # )

    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        await http.close()

# ---------------------------- UI SETUP ------------------------------- #
asyncio.run(main())
