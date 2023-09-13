from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Playlist, User, Song, Artist, Album, Genre, PlaylistSongs, UserPlaylists

DATABASE_URI = 'sqlite:///music.db'
engine = create_engine(DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def create_sample_data():
    artist1 = Artist(artist_name="Gabzy")
    artist2 = Artist(artist_name="Melvitto")

    album1 = Album(album_title="Summers", artist=artist1)
    album2 = Album(album_title="THENIGHTISYOUNG", artist=artist2)
    album3 = Album(album_title="soon", artist=artist1)
    album4 = Album(album_title="soon", artist=artist2)
    
    genre1 = Genre(genre_name="Pop")
    genre2 = Genre(genre_name="Rock")

    user1 = User(user_name="Kamente")
    user2 = User(user_name="Justin")

    playlist1 = Playlist(playlist_name="Gabzzy & Melvitto")
    playlist2 = Playlist(playlist_name="Playlist 2")

    song1 = Song(song_title="Come Over", song_duration=240, album=album1, artist=artist1, genre=genre1)
    song2 = Song(song_title="Wait For You", song_duration=180, album=album2, artist=artist2, genre=genre2)
    song3 = Song(song_title="Stay", song_duration=300, album=album3, artist=artist1, genre=genre2)
    song4 = Song(song_title="In Fact", song_duration=210, album=album4, artist=artist2, genre=genre1)

    playlist1.songs.append(song1)
    playlist2.songs.append(song2)
    playlist1.songs.append(song3)
    playlist2.songs.append(song4)

    user1.playlists.append(playlist1)
    user2.playlists.append(playlist2)

    session.add_all([artist1, artist2, album1, album2, album3, album4, genre1, genre2, user1, user2, 
                     playlist1, playlist2, song1, song2, song3, song4])


    session.commit()

if __name__ == '__main__':
    create_sample_data()

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from models import Playlist, PlaylistSongs, User, UserPlaylists, Artist, Album, Song, Genre 

# DATABASE_URI = 'sqlite:///music.db'
# engine = create_engine(DATABASE_URI, echo = True)
# Session = sessionmaker
# session = Session

# def create_data ():
#     artist1 = Artist(artist_name = "Gabzy")
#     artist2 = Artist(artist_name = "Khalid")
    
#     album1 = Album(album_title = "MasterMind", artist = artist1)
#     album2 = Album(album_title = "Summers", artist = artist2)
    
    
#     genre1 = Genre(genre_name = "HipHop")
#     genre2 = Genre(genre_name = "Pop")
    
#     user1 = User(user_name = "Kamente")
#     user2 = User(user_name = "Justin")
    
#     playlist1 = Playlist(playlist_name = "MyPlaylist")
    
#     song1 = Song(song_title = "Come Over", song_duration = 200, album=album1, artist = artist1, genre = genre1)
#     song1 = Song(song_title = "Eastside", song_duration = 270, album=album2, artist = artist2, genre = genre2)

#     playlist1.songs.append(song1)
#     playlist1.songs.append(song2)
    
#     user1.playlists.append(playlist1)
#     user2.playlists.append(playlist1)
    
#     session.add_all(user1, user2, artist1, artist2, genre1, genre2, album1, album2, song1, song2, playlist1)
#     session.commit()
    
#     if __name__ == '__main__':
#         create_data()