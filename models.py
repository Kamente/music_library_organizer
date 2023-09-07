from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey


DATABASE_URI = 'sqlite:///music.db'
engine = create_engine(DATABASE_URI, echo=True)
Base = declarative_base()


class Artist(Base):
    __tablename__ = 'artists'
    artist_id = Column(Integer, primary_key=True)
    artist_name = Column(String)
    
    def __repr__(self):
        return f'Artist (artist_id = {self.artist_id},' +\
            f'artist_name = {self.artist_name}'
            

class Albums(Base):
    __tablename__ = 'albums'
    album_id = Column(Integer, primary_key=True)
    album_title = Column(String)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))
    
    def __repr__(self):
        return f'Album(album_id = {self.album_id}, '+\
            f'album_title = {self.album_title}, '+\
                f'artist_id = {self.artist_id}'
    
class Genres(Base):
    __tablename__ = 'genres'
    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String)
    
    def __repr__(self): 
        return f'Genre(genre_id = {self.genre_id}, ' +\
            f'genre_name = {self.genre_name}'


class Playlists(Base):
    __tablename__ = 'playlists'
    playlist_id = Column(Integer, primary_key=True)
    playlist_title = Column(String)
    
    def __repr__(self):
        return f'Playlist(playlist_id = {self.playlist_id},' +\
            f'playlist_title = {self.playlist_title}'

class Songs(Base):
    __tablename__ = 'songs'
    song_id = Column(Integer, primary_key=True)
    song_title = Column(String)
    song_duration = Column(Integer)
    album_id = Column(Integer, ForeignKey('albums.album_id'))
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))
    genre_id = Column(Integer, ForeignKey('genres.genre_id'))
    
    def __repr__(self):
          return f'Song(song_id={self.song_id},'+\
            f'song_title="{self.song_title}", '+\
               f'song_duration={self.song_duration},'+\
                   f'album_id={self.album_id},'+\
                       f'artist_id={self.artist_id},'+\
                           f'genre_id={self.genre_id})'

        
class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    
    def __repr__(self):
        return f'User(user_id={self.user_id},'+\
            f'user_name="{self.user_name}")'


class PlaylistsSongs(Base):
    __tablename__ = 'playlists_songs'
    playlists_songs_id = Column(Integer, primary_key=True)
    playlist_id = Column(Integer, ForeignKey('playlists.playlist_id'))
    song_id = Column(Integer, ForeignKey('songs.song_id'))
    
 
    def __repr__(self):
        return f'PlaylistsSongs(playlists_songs_id={self.playlists_songs_id}, ' + \
            f'playlist_id={self.playlist_id},' +\
                f'song_id={self.song_id})'

class UserPlaylists(Base):
    __tablename__ = 'user_playlists'
    user_playlist_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    playlists_id = Column(Integer, ForeignKey('playlists.playlist_id'))

    def __repr__(self):
        return f'UserPlaylists(user_playlist_id={self.user_playlist_id},' +\
            f'user_id={self.user_id},' +\
                f'playlists_id={self.playlists_id})'

Base.metadata.create_all(bind=engine)
Session = session_maker(bind=engine)
session = Session