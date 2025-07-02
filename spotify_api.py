import json
import time
import requests
from requests.exceptions import SSLError, ConnectionError, Timeout

from logger import logger
from config import MAX_RETIRES, RETRY_BACKOFF

def error_handling(headers: str, url: str, error_message: str = "", retries: int = MAX_RETIRES, backoff: int = RETRY_BACKOFF) -> dict:
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 5))
                logger.warning(f"[Rate limited] Waiting {retry_after}s. {error_message}")
                time.sleep(retry_after)
                continue

            if response.status_code == 401:
                logger.error(f"[Unauthorized] Token invalid or expired. {error_message}")
                return {}

            if response.status_code != 200:
                logger.error(f"[HTTP Error {response.status_code}] {error_message}")
                return {}

            return response.json()

        except (SSLError, ConnectionError, Timeout) as e:
            logger.warning(f"[Network Error] {type(e).__name__} on attempt {attempt+1}. Retrying in {backoff}s...")
            time.sleep(backoff)

        except json.JSONDecodeError:
            logger.error(f"[Parse Error] Invalid JSON. {error_message}")
            return {}

    logger.error(f"[Failed] All {retries} attempts failed. {error_message}")
    return {}

def search_artists_by_genre (headers:str, genre:str, results_per_page:int, offset:int)-> list:
    url = "https://api.spotify.com/v1/search"
    query = f"?q='genre:{genre}'&type=artist&limit={results_per_page}&offset={offset}"
    query_url = url + query

    response = error_handling(headers, query_url)

    return response["artists"]["items"]

def get_albums_by_artist(headers:str, artist_id:str, results_per_page:int, offset:int) -> list:
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    query = f"?include_groups=album,single,compilation,appears_on&limit={results_per_page}&offset={offset}"
    query_url = url + query

    response = error_handling(headers, query_url, f"artist id: {artist_id}")

    return response["items"]

def get_several_albums_tracks(headers:str, albums_ids:str) -> list:
    url = "https://api.spotify.com/v1/albums"
    query = f"?ids={albums_ids}"
    query_url = url + query

    response = error_handling(headers, query_url)

    return response["albums"]

def get_several_track_information(headers:str, tracks_ids:str) -> list:
    url = "https://api.spotify.com/v1/tracks"
    query = f"?ids={tracks_ids}"
    query_url = url + query

    response = error_handling(headers, query_url)

    return response["tracks"]
