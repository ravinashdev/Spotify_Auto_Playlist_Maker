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
from clients.wiki import WikiClient
from clients.soup import SoupClient

# ---------------------------- CONSTANTS ------------------------------- #
http = HTTPClient()
spotify = SpotifyClient(http, settings)
wikipedia = WikiClient(http, settings)
soup = SoupClient()

# ---------------------------- GLOBAL VARIABLES ------------------------------- #

# ---------------------------- FUNCTIONS ------------------------------- #
async def main(**kwargs):
    try:

        # Scapper Client
        # hot_100_response = await soup.get_soup("/2000-08-12/")
        # print(hot_100_response.prettify())

        # Wikipedia API Series Calls
        wikipedia_get_title = await wikipedia.get_title(
            f"Billboard_Year-End_Hot_100_singles_of_{kwargs.get('year')}"
        )
        # print(json.dumps(wikipedia_get_title, indent=4))
        wikipedia_make_soup = soup.make_soup(
            json_data=wikipedia_get_title
        )
        # print(wikipedia_make_soup.prettify())
        table = wikipedia_make_soup.find("table", class_="wikitable")
        rows = table.find_all("tr")[1:]
        top_100_songs_of_given_year = []
        for row in rows:
            # only call once
            cols = row.find_all("td")
            if len(cols) < 3:
                #skip bad rows
                continue
            try:
                rank = int(cols[0].get_text(strip=True))
            except ValueError:
                # skip rows where rank isn't a number
                continue
            title = cols[1].get_text(strip=True).strip('"')
            artist = cols[2].get_text(strip=True)
            new_dict = {
                "rank": rank,
                "title": title,
                "artist": artist,
            }
            top_100_songs_of_given_year.append(new_dict)
        print(top_100_songs_of_given_year)

        # Spotify API Series Calls
        # spotify_get_artist_data_response = await spotify.get_artist(
        #     artist_id="0TnOYISbd1XYRBk9myaseg",
        # )
        # print(json.dumps(spotify_get_artist_data_response, indent=4))
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
user_input = int(input("What year of music brings you back? "))
asyncio.run(main(year=user_input))
