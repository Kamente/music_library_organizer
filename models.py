from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import mapper

DATABASE_URI = 'sqlite:///music.db'
engine = create_engine(DATABASE_URI, echo=True)
Base = declarative_base()

# Define the association table for playlist and songs
class PlaylistSongs(Base):
    __tablename__ = 'playlist_songs'
    playlist_id = Column(Integer, ForeignKey('playlists.playlist_id'), primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.song_id'), primary_key=True)

# Define the association table for user and playlists
class UserPlaylists(Base):
    __tablename__ = 'user_playlists'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    playlist_id = Column(Integer, ForeignKey('playlists.playlist_id'), primary_key=True)

class Artist(Base):
    __tablename__ = 'artists'
    artist_id = Column(Integer, primary_key=True)
    artist_name = Column(String)
    
    # One-to-Many relationship: Artist to Albums
    albums = relationship('Album', back_populates='artist')
    
    # One-to-Many relationship: Artist to Songs
    songs = relationship('Song', back_populates='artist')

    def __repr__(self):
        return f'Artist(artist_id={self.artist_id}, ' + \
            f'artist_name="{self.artist_name}")'


class Album(Base):
    __tablename__ = 'albums'
    album_id = Column(Integer, primary_key=True)
    album_title = Column(String)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))
    
    # Many-to-One relationship: Albums to Artist
    artist = relationship('Artist', back_populates='albums')
    
    # One-to-Many relationship: Album to Songs
    songs = relationship('Song', back_populates='album')

    def __repr__(self):
        return f'Album(album_id = {self.album_id},' +\
            f'album_title = {self.album_title}, '+\
                f'artist_id = {self.artist_id})'
    
class Genre(Base):
    __tablename__ = 'genres'
    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String)
    
    # One-to-Many relationship: Genre to Songs
    songs = relationship('Song', back_populates='genre')

    def __repr__(self):
        return f'Genre(genre_id = {self.genre_id},'+\
            f'genre_name = {self.genre_name})'

class Playlist(Base):
    __tablename__ = 'playlists'
    playlist_id = Column(Integer, primary_key=True)
    playlist_title = Column(String)
    
    # Many-to-Many relationship: Playlists to Songs
    songs = relationship('Song', secondary='playlist_songs', back_populates='playlists')
    
    # Many-to-Many relationship: Playlists to Users
    users = relationship('User', secondary='use', back_populates='playlists')

    def __repr__(self):
        return f'Playlist(playlist_id = {self.playlist_id}, '+\
            f'playlist_title = {self.playlist_title})'

class Song(Base):
    __tablename__ = 'songs'
    song_id = Column(Integer, primary_key=True)
    song_title = Column(String)
    song_duration = Column(Integer)
    album_id = Column(Integer, ForeignKey('albums.album_id'))
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))
    genre_id = Column(Integer, ForeignKey('genres.genre_id'))
    
    # Many-to-One relationship: Songs to Album
    album = relationship('Album', back_populates='songs')
    
    # Many-to-One relationship: Songs to Artist
    artist = relationship('Artist', back_populates='songs')
    
    # Many-to-One relationship: Songs to Genre
    genre = relationship('Genre', back_populates='songs')
    
    # Many-to-Many relationship: Songs to Playlists
    playlists = relationship('Playlist', secondary='playlist_songs', back_populates='songs')

    def __repr__(self):
          return f'Song(song_id={self.song_id},'+\
              f'song_title="{self.song_title}",'+\
                  f'song_duration={self.song_duration},'+\
                      f'album_id={self.album_id},'+\
                          f'artist_id={self.artist_id},'+\
                              f'genre_id={self.genre_id})'

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    
    # Many-to-Many relationship: Users to Playlists
    playlists = relationship('Playlist', secondary='use', back_populates='users')

    def __repr__(self):
        return f'User(user_id={self.user_id},'+\
            f'user_name="{self.user_name}")'

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
