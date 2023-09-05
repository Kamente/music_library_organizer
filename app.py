from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session_maker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey


DATABASE_URI = 'sqlite:///music.db'
engine = create_engine(DATABASE_URI, echo=True)
Base = declarative_base()


class Artist(Base):
    __tablename__ = 'artists'
    artist_id = Column(Integer, primary_key=True)
    artist_name = Column(String)


class Albums(Base):
    __tablename__ = 'albums'
    album_id = Column(Integer, primary_key=True)
    album_title = Column(String)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))


class Genres(Base):
    __tablename__ = 'genres'
    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(Integer)


class Playlists(Base):
    __tablename__ = 'playlists'
    playlist_id = Column(Integer, primary_key=True)
    playlist_title = Column(String)


class Songs(Base):
    __tablename__ = 'songs'
    song_id = Column(Integer, primary_key=True)
    song_title = Column(String)
    song_duration = Column(Integer)
    album_id = Column(Integer, ForeignKey('albums.album_id'))
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))
    genre_id = Column(Integer, ForeignKey('genres.genre_id'))


class users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)


class playlists_songs(Base):
    __tablename__ = 'playlists_songs'
    playlists_songs_id = Column(Integer, primary_key=True)
    playlist_id = Column(Integer, ForeignKey('playlists.playlist.id'))
    song_id = Column(Integer, ForeignKey('songs.song.id'))


class user_playlists(Base):
    __tablename__ = 'user_playlists'
    user_playlist_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    playlists_id = Column(Integer, ForeignKey('playlists.playlist_id'))


Base.metadata.create_all(bind=engine)
Session = session_maker(bind=engine)
session = Session
