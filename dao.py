from typing import List
from sqlmodel import Session, select
from db import engine
from models import Artist, Album, Track

def dao_get_all_artists() -> List[Artist]:
    with Session(engine) as session:
        statement = select(Artist)
        artists = session.exec(statement).all()
        return artists

def dao_fetch_artist(artist_id: str) -> Artist:
    with Session(engine) as session:
        existing_artist = session.exec(
            select(Artist).where(Artist.spotify_id == artist_id)
        ).first()
        if existing_artist:
            return existing_artist
        else:
            return None

def dao_save_artist(artist: Artist) -> None:
    with Session(engine) as session:
        if not dao_fetch_artist(artist.spotify_id):
            session.add(artist)       
        session.commit()

def dao_get_all_albums() -> List[Album]:
    with Session(engine) as session:
        statement = select(Album)
        albums = session.exec(statement).all()
        return albums

def dao_fetch_album(album_id: str) -> Album:
    with Session(engine) as session:
        existing_album = session.exec(
            select(Album).where(Album.spotify_id == album_id)
        ).first()
        if existing_album:
            return existing_album
        else:
            return None

def dao_save_album(album: Album) -> None:
    with Session(engine) as session:
        if not dao_fetch_album(album.spotify_id):
            session.add(album)       
        session.commit()

def dao_update_album(album_id: str, album_popularity, album_tracks) -> None:
    with Session(engine) as session:
        selected_album = dao_fetch_album(album_id)
        selected_album.popularity = album_popularity
        selected_album.tracks = album_tracks        
        session.add(selected_album)
        session.commit()

def dao_get_all_tracks() -> List[Track]:
    with Session(engine) as session:
        statement = select(Track)
        tracks = session.exec(statement).all()
        return tracks

def dao_fetch_track(track_id: str) -> Track:
    with Session(engine) as session:
        existing_track = session.exec(
            select(Track).where(Track.spotify_id == track_id)
        ).first()
        if existing_track:
            return existing_track
        else:
            return None
        
def dao_save_track(track: Track) -> None:
    with Session(engine) as session:
        if not dao_fetch_track(track.spotify_id):
            session.add(track)       
        session.commit()

def dao_update_track(track_id: str, track_popularity: int) -> None:
    with Session(engine) as session:
        selected_track = dao_fetch_track(track_id)
        selected_track.popularity = track_popularity
        session.add(selected_track)
        session.commit()