import json
import time
import requests
from requests.exceptions import SSLError, ConnectionError, Timeout

# from auth import get_token
from auth import SpotifyAuthManager
from logger import logger
from config import MAX_RETRIES, RETRY_BACKOFF  # fixed typo here


def get_with_error_handling(auth: SpotifyAuthManager,url: str, params: dict = None, error_message: str = "", retries: int = MAX_RETRIES, backoff: int = RETRY_BACKOFF) -> dict:
    for attempt in range(retries):
        try:
            headers = auth.get_headers()
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 5))
                logger.warning(f"[Rate limited] Waiting {retry_after}s. {error_message}")
                time.sleep(retry_after)
                continue

            if response.status_code == 401:
                logger.error(f"[Unauthorized] Token invalid or expired while {error_message}")
                auth.get_token()
                continue

            if response.status_code != 200:
                logger.error(f"[HTTP Error {response.status_code}] while {error_message}")
                return {}
            return response.json()

        except (SSLError, ConnectionError, Timeout) as e:
            logger.warning(f"[Network Error] {type(e).__name__} on attempt {attempt+1}. Retrying in {backoff}s...")
            time.sleep(backoff)

        except json.JSONDecodeError:
            logger.error(f"[Parse Error] Invalid JSON while {error_message}")
            return {}

    logger.error(f"[Failed] All {retries} attempts failed while {error_message}")
    return {}

def get_several_artists(auth: SpotifyAuthManager, artists_ids: str) -> list:
    url = "https://api.spotify.com/v1/artists"
    params = {
        "ids": artists_ids
    }
    response = get_with_error_handling(auth, url, params=params, error_message=f"getting artist: '{artists_ids}'")
    return response.get("artists", [])



def search_artists(auth: SpotifyAuthManager, query: str, results_per_page: int, offset: int) -> list:
    url = "https://api.spotify.com/v1/search"
    params = {
        "q": query,
        "type": "artist",
        "limit": results_per_page,
        "offset": offset
    }
    response = get_with_error_handling(auth, url, params=params, error_message=f"searching artists for query: '{query}', offset {offset}")
    return response.get("artists", {}).get("items", [])


def get_albums_by_artist(auth: SpotifyAuthManager, artist_id: str, results_per_page: int, offset: int) -> list:
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    params = {
        "include_groups": "album,single,compilation,appears_on",
        "limit": results_per_page,
        "offset": offset
    }
    response = get_with_error_handling(auth, url, params=params, error_message=f"fetching albums for artist id: {artist_id}")
    return response.get("items", [])


def get_several_albums_tracks(auth: SpotifyAuthManager, albums_ids: str) -> list:
    url = "https://api.spotify.com/v1/albums"
    params = {
        "ids": albums_ids
    }
    response = get_with_error_handling(auth, url, params=params, error_message=f"fetching tracks for albums: {albums_ids}")
    return response.get("albums", [])


def get_several_track_information(auth: SpotifyAuthManager, tracks_ids: str) -> list:
    url = "https://api.spotify.com/v1/tracks"
    params = {
        "ids": tracks_ids
    }
    response = get_with_error_handling(auth, url, params=params, error_message=f"fetching info for tracks: {tracks_ids}")
    return response.get("tracks", [])
