from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import Column, Integer, String

DATABASE_URI = 'sqlite:///music.db'
engine = create_engine(DATABASE_URI, echo=True)
Base = declarative_base()

class PlaylistSongs(Base):
    __tablename__ = 'playlist_songs'
    playlist_id = Column(Integer, ForeignKey('playlists.playlist_id'), primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.song_id'), primary_key=True)

class UserPlaylists(Base):
    __tablename__ = 'user_playlists'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    playlist_id = Column(Integer, ForeignKey('playlists.playlist_id'), primary_key=True)

    user = relationship('User', back_populates='playlists')
    playlist = relationship('Playlist', back_populates='users')

class Artist(Base):
    __tablename__ = 'artists'
    artist_id = Column(Integer, primary_key=True)
    artist_name = Column(String)
    
    songs = relationship('Song', back_populates='artist_obj')

    def __repr__(self):
        return f'Artist(artist_id={self.artist_id}, ' + \
            f'artist_name="{self.artist_name}")'

class Album(Base):
    __tablename__ = 'albums'
    album_id = Column(Integer, primary_key=True)
    album_title = Column(String)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))

    artist = relationship('Artist', back_populates='albums')

    songs = relationship('Song', back_populates='album') 

    def __repr__(self):
        return f'Album(album_id={self.album_id}, ' +\
            f'album_title="{self.album_title}", '+\
            f'artist_id={self.artist_id})'

class Song(Base):
    __tablename__ = 'songs'
    song_id = Column(Integer, primary_key=True)
    song_title = Column(String)
    song_duration = Column(Integer)
    album_id = Column(Integer, ForeignKey('albums.album_id'))
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))
    genre_id = Column(Integer, ForeignKey('genres.genre_id'))

    album = relationship('Album', back_populates='songs')  
    artist = relationship('Artist', back_populates='songs_obj', foreign_keys='[Song.artist_id]')
    genre = relationship('Genre', back_populates='songs_obj', foreign_keys='[Song.genre_id]')
    playlists = relationship('Playlist', secondary='playlist_songs', back_populates='songs_obj')

    def __repr__(self):
        return f'Song(song_id={self.song_id}, ' +\
            f'song_title="{self.song_title}", ' +\
            f'song_duration={self.song_duration}, ' +\
            f'album_id={self.album_id}, ' +\
            f'artist_id={self.artist_id}, ' +\
            f'genre_id={self.genre_id})'

class Genre(Base):
    __tablename__ = 'genres'
    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String)
    
    songs = relationship('Song', back_populates='song_genre')

    def __repr__(self):
        return f'Genre(genre_id={self.genre_id}, ' +\
            f'genre_name="{self.genre_name}")'

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)

    playlists = relationship('Playlist', secondary='user_playlists', back_populates='users') 

    def __repr__(self):
        return f'User(user_id={self.user_id}, user_name="{self.user_name}")'

class Playlist(Base):
    __tablename__ = 'playlists'
    playlist_id = Column(Integer, primary_key=True)
    playlist_name = Column(String)

    users = relationship('User', secondary='user_playlists', back_populates='playlists') 
    songs = relationship('Song', secondary='playlist_songs', back_populates='playlists_obj')

    def __repr__(self):
        return f'Playlist(playlist_id={self.playlist_id}, playlist_name="{self.playlist_name}")'

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
