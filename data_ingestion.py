from spotify_api import search_artists_by_genre, get_albums_by_artist, get_several_albums_tracks, get_several_track_information
from models import Artist, Album, Track
from dao import dao_get_all_artists, dao_save_artist, dao_get_all_albums, dao_save_album, dao_get_all_tracks, dao_save_track, dao_update_album, dao_update_track
from tqdm import tqdm
from joblib import Parallel, delayed

from config import N_JOBS, N_SEVERAL_ALBUMS, N_SEVERAL_TRACKS

def extract_artists(headers: str, genre_query: str, max_results: int, results_per_page: int) -> None:
    for offset in tqdm(range (0, max_results, results_per_page)):
        artists = search_artists_by_genre(headers, genre_query, results_per_page, offset)
        if not artists:
            continue

        for artist in artists:
            artist_instance = Artist(
                spotify_id = artist["id"],
                name = artist["name"],
                popularity = artist["popularity"],
                followers = artist["followers"]["total"]
            )
            dao_save_artist(artist_instance)
            
def parallel_extract_artists(headers: str, genre_query: str, max_results: int, results_per_page: int) -> None:
    artists = Parallel(n_jobs=N_JOBS)(
        delayed(search_artists_by_genre)(headers, genre_query, results_per_page, offset)
          for offset in 
          tqdm(range (0, max_results, results_per_page))
        )
    for artist in artists[0]:
        artist_instance = Artist(
            spotify_id = artist["id"],
            name = artist["name"],
            popularity = artist["popularity"],
            followers = artist["followers"]["total"]
        )
        dao_save_artist(artist_instance)

def parallel_extract_albums(headers: str, max_results: int, results_per_page: int) -> None:
    artists = dao_get_all_artists()
    for artist in tqdm(artists):
        albums = Parallel(n_jobs=N_JOBS)(
            delayed(get_albums_by_artist)(headers, artist.spotify_id, results_per_page, offset)
              for offset in 
              tqdm(range (0, max_results, results_per_page), colour="yellow", leave = False))
        
        for album in albums[0]:
                artists = album["artists"]
                album_artists = ""
                for item in artists:
                    if item == artists[0]:
                        album_artists = album_artists + f"{item['name']}"
                    else:
                        album_artists = album_artists + f", {item['name']}"

                album_instance = Album(
                    spotify_id = album["id"],
                    title = album["name"],
                    tracks= 0,
                    artists = album_artists,
                    popularity = 0
                )
                dao_save_album(album_instance)

def extract_tracks_by_albums(headers: str) -> None:
    all_albums = dao_get_all_albums()
    albums_ids = []

    for i in range(0, len(all_albums), N_SEVERAL_ALBUMS):
        albums_ids_str = ""
        temp_album_list = all_albums[i:N_SEVERAL_ALBUMS]
        for album in temp_album_list:
            if albums_ids_str == "":
                albums_ids_str = albums_ids_str +  album.spotify_id
            else:
                albums_ids_str = albums_ids_str + "," + album.spotify_id

        albums_ids.append(albums_ids_str)


    albums_json = Parallel(n_jobs=N_JOBS)(
        delayed(get_several_albums_tracks)(headers, id)
        for id in 
        tqdm(albums_ids)
    )
    
    for album_json in albums_json[0]:
        dao_update_album(album_json["id"], album_json["popularity"], album_json["tracks"]["total"])

        tracks = album_json["tracks"]["items"]
        for track in tracks:

            artists = track["artists"]
            track_artists = ""
            for artist in artists:
                if artist == artists[0]:
                    track_artists = track_artists + f"{artist['name']}"
                else:
                    track_artists = track_artists + f", {artist['name']}"
            
            track_instance = Track(
                spotify_id = track["id"],
                title = track["name"],
                popularity = 0,
                duration_ms = track["duration_ms"],
                album_title = album_json["name"],
                album_spotify_id = album_json["id"],
                artists = track_artists
            )
            dao_save_track(track_instance) 

def extract_several_tracks_info(headers:str) -> None:
    all_tracks = dao_get_all_tracks()
    tracks_ids = []

    for i in range(0, len(all_tracks), N_SEVERAL_TRACKS):
        tracks_ids_str = ""
        temp_tracks_list = all_tracks[i:N_SEVERAL_TRACKS]
        for track in temp_tracks_list:
            if tracks_ids_str == "":
                tracks_ids_str = tracks_ids_str +  track.spotify_id
            else:
                 tracks_ids_str = tracks_ids_str + "," +  track.spotify_id

        tracks_ids.append(tracks_ids_str)

    tracks_json = Parallel(n_jobs=N_JOBS)(
        delayed(get_several_track_information)(headers, id)
        for id in 
        tqdm(tracks_ids)
    )

    for track_json in tracks_json[0]:
        dao_update_track(track_json["id"], track_json["popularity"])