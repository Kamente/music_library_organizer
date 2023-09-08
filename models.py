from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String

DATABASE_URI = 'sqlite:///music.db'
engine = create_engine(DATABASE_URI, echo=True)
Base = declarative_base()

class PlaylistSongs(Base):
    __tablename__ = 'playlist_songs'
    playlist_id = Column(Integer, ForeignKey('playlists.playlist_id'), primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.song_id'), primary_key=True)

class Playlist(Base):
    __tablename__ = 'playlists'
    playlist_id = Column(Integer, primary_key=True)
    playlist_name = Column(String)

    users = relationship('User', secondary='user_playlists', back_populates='playlists') 
    songs = relationship('Song', secondary='playlist_songs', back_populates='playlists')
    user_playlists = relationship('UserPlaylists', back_populates='playlist')

    def _repr_(self):
        return f'Playlist(playlist_id={self.playlist_id}, playlist_name="{self.playlist_name}")'

class UserPlaylists(Base):
    __tablename__ = 'user_playlists'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    playlist_id = Column(Integer, ForeignKey('playlists.playlist_id'), primary_key=True)

    user = relationship('User', back_populates='user_playlists')  
    playlist = relationship('Playlist', back_populates='user_playlists')  

    def _init_(self, user=None, playlist=None):
        self.user = user
        self.playlist = playlist

class Artist(Base):
    __tablename__ = 'artists'
    artist_id = Column(Integer, primary_key=True)
    artist_name = Column(String)
    
    songs = relationship('Song', back_populates='artist')
    albums = relationship('Album', back_populates='artist')

    def _repr_(self):
        return f'Artist(artist_id={self.artist_id}, artist_name="{self.artist_name}")'

class Album(Base):
    __tablename__ = 'albums'
    album_id = Column(Integer, primary_key=True)
    album_title = Column(String)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))

    artist = relationship('Artist', back_populates='albums')

    songs = relationship('Song', back_populates='album') 

    def _repr_(self):
        return f'Album(album_id={self.album_id}, album_title="{self.album_title}", artist_id={self.artist_id})'

class Song(Base):
    __tablename__ = 'songs'
    song_id = Column(Integer, primary_key=True)
    song_title = Column(String)
    song_duration = Column(Integer)
    album_id = Column(Integer, ForeignKey('albums.album_id'))
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))
    genre_id = Column(Integer, ForeignKey('genres.genre_id'))

    album = relationship('Album', back_populates='songs')  
    artist = relationship('Artist', back_populates='songs', foreign_keys='[Song.artist_id]')
    genre = relationship('Genre', back_populates='songs')

    playlists = relationship('Playlist', secondary='playlist_songs', back_populates='songs')

    def _repr_(self):
        return f'Song(song_id={self.song_id}, song_title="{self.song_title}", song_duration={self.song_duration}, album_id={self.album_id}, artist_id={self.artist_id}, genre_id={self.genre_id})'

class Genre(Base):
    __tablename__ = 'genres'
    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String)
    
    songs = relationship('Song', back_populates='genre')

    def _repr_(self):
        return f'Genre(genre_id={self.genre_id}, genre_name="{self.genre_name}")'

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)

    playlists = relationship('Playlist', secondary='user_playlists', back_populates='users')

    user_playlists = relationship('UserPlaylists', back_populates='user') 

    def _repr_(self):
        return f'User(user_id={self.user_id}, user_name="{self.user_name}")'


Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()