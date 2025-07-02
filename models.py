from sqlmodel import Field, SQLModel

class Artist(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    spotify_id: str
    name: str
    popularity: int
    followers: int

class Album(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    spotify_id: str
    title: str
    tracks: int
    popularity: int
    artists: str

class Track(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    spotify_id: str
    title: str
    popularity: int
    duration_ms: int
    album_title: str
    album_spotify_id: str
    artists: str