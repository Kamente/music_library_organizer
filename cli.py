import click
from tabulate import tabulate 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Playlist, Song, User, Artist, Album, Genre, UserPlaylists, PlaylistSongs

DATABASE_URI = 'sqlite:///music.db'

engine = create_engine(DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def prompt_for_missing_args(args, arg_names):
    missing_args = [name for name, value in zip(arg_names, args) if value is None]
    for name in missing_args:
        args[arg_names.index(name)] = click.prompt(f'Enter the {name.replace("_", " ").title()}:')

@click.group()
def cli():
    pass

@cli.command()
@click.argument('playlist_name', required=False)
def create_playlist(playlist_name):
    if not playlist_name:
        playlist_name = click.prompt('Enter the playlist name:')
    new_playlist = Playlist(playlist_name=playlist_name)
    session.add(new_playlist)
    session.commit()
    print(f'Playlist "{playlist_name}" created successfully.')

@cli.command()
@click.argument('song_title')
@click.argument('song_duration')
@click.option('--album_id', default=None, help='Album ID if applicable')
@click.option('--artist_id', default=None, help='Artist ID if applicable')
@click.option('--genre_id', default=None, help='Genre ID if applicable')
def add_song(song_title, song_duration, album_id, artist_id, genre_id):
    args = [song_title, song_duration, album_id, artist_id, genre_id]
    arg_names = ['song_title', 'song_duration', 'album_id', 'artist_id', 'genre_id']
    prompt_for_missing_args(args, arg_names)
    
    new_song = Song(
        song_title=args[0],
        song_duration=args[1],
        album_id=args[2],
        artist_id=args[3],
        genre_id=args[4]
    )
    session.add(new_song)
    session.commit()
    print(f'Song "{args[0]}" added successfully.')

@cli.command()
@click.argument('user_name', required=False)
def create_user(user_name):
    if not user_name:
        user_name = click.prompt('Enter the user name:')
    new_user = User(user_name=user_name)
    session.add(new_user)
    session.commit()
    print(f'User "{user_name}" created successfully.')

@cli.command()
@click.argument('artist_name', required=False)

def create_artist(artist_name):
    if not artist_name:
        artist_name = click.prompt('Enter the artist name:')
    new_artist = Artist(artist_name=artist_name)
    session.add(new_artist)
    session.commit()
    print(f'Artist "{artist_name}" created successfully.')

@cli.command()
@click.argument('album_title', required=False)
@click.argument('artist_id', required=False)
def create_album(album_title, artist_id):
    if not album_title:
        album_title = click.prompt('Enter the album title:')
    if not artist_id:
        artist_id = click.prompt('Enter the artist ID:')
    new_album = Album(album_title=album_title, artist_id=artist_id)
    session.add(new_album)
    session.commit()
    print(f'Album "{album_title}" created successfully.')

@cli.command()
@click.argument('genre_name', required=False)
def create_genre(genre_name):
    if not genre_name:
        genre_name = click.prompt('Enter the genre name:')
    new_genre = Genre(genre_name=genre_name)
    session.add(new_genre)
    session.commit()
    print(f'Genre "{genre_name}" created successfully.')

@cli.command()
@click.argument('user_id', required=False)
@click.argument('playlist_id', required=False)
def create_user_playlist(user_id, playlist_id):
    if not user_id:
        user_id = click.prompt('Enter the user ID:')
    if not playlist_id:
        playlist_id = click.prompt('Enter the playlist ID:')
    new_user_playlist = UserPlaylists(user_id=user_id, playlist_id=playlist_id)
    session.add(new_user_playlist)
    session.commit()
    print(f'User Playlist created successfully.')

@cli.command()
@click.argument('playlist_id', required=False)
@click.argument('song_id', required=False)
def add_song_to_playlist(playlist_id, song_id):
    if not playlist_id:
        playlist_id = click.prompt('Enter the playlist ID:')
    if not song_id:
        song_id = click.prompt('Enter the song ID:')
    new_playlist_song = PlaylistSongs(playlist_id=playlist_id, song_id=song_id)
    session.add(new_playlist_song)
    session.commit()
    print(f'Song added to playlist successfully.')

@cli.command()
def list_users():
    users = session.query(User).all()
    user_data = [(user.user_id, user.user_name) for user in users]
    headers = ["User ID", "User Name"]
    table = tabulate(user_data, headers, tablefmt="grid")
    print("List of Users:")
    print(table)

@cli.command()
def list_artists():
    artists = session.query(Artist).all()
    artist_data = [(artist.artist_id, artist.artist_name) for artist in artists]
    headers = ["Artist ID", "Artist Name"]
    table = tabulate(artist_data, headers, tablefmt="grid")
    print("List of Artists:")
    print(table)

@cli.command()
def list_albums():
    albums = session.query(Album).all()
    album_data = [(album.album_id, album.album_title, album.artist.artist_name) for album in albums]
    headers = ["Album ID", "Album Title", "Artist Name"]
    table = tabulate(album_data, headers, tablefmt="grid")
    print("List of Albums:")
    print(table)

@cli.command()
def list_genres():
    genres = session.query(Genre).all()
    genre_data = [(genre.genre_id, genre.genre_name) for genre in genres]
    headers = ["Genre ID", "Genre Name"]
    table = tabulate(genre_data, headers, tablefmt="grid")
    print("List of Genres:")
    print(table)

@cli.command()
def list_playlists():
    playlists = session.query(Playlist).all()
    playlist_data = [(playlist.playlist_id, playlist.playlist_name) for playlist in playlists]
    headers = ["Playlist ID", "Playlist Name"]
    table = tabulate(playlist_data, headers, tablefmt="grid")
    print("List of Playlists:")
    print(table)

@cli.command()
def list_user_playlists():
    user_playlists = session.query(UserPlaylists).all()
    user_playlist_data = [(user_playlist.user_id, user_playlist.playlist_id) for user_playlist in user_playlists]
    headers = ["User ID", "Playlist ID"]
    table = tabulate(user_playlist_data, headers, tablefmt="grid")
    print("List of User Playlists:")
    print(table)

@cli.command()
def list_songs():
    songs = session.query(Song).all()
    song_data = [
        (song.song_id, song.song_title, song.album.album_title, song.artist.artist_name, song.genre.genre_name)
        for song in songs
    ]

    headers = ["Song ID", "Song Title", "Album Title", "Artist Name", "Genre Name"]

    table = tabulate(song_data, headers, tablefmt="grid")

    print("List of Songs:")
    print(table)  

@cli.command()
def list_playlist_songs():
    playlist_table = Playlist.__table__
    playlist_songs_table = PlaylistSongs.__table__
    song_table = Song.__table__

    query = session.query(Playlist.playlist_name, Song.song_title). \
        select_from(playlist_table). \
        join(playlist_songs_table, playlist_table.c.playlist_id == playlist_songs_table.c.playlist_id). \
        join(song_table, playlist_songs_table.c.song_id == song_table.c.song_id). \
        order_by(Playlist.playlist_name, Song.song_title)

    playlist_songs = query.all()

    playlist_song_data = [(playlist_name, song_title) for playlist_name, song_title in playlist_songs]

    headers = ["Playlist Name", "Song Title"]
    table = tabulate(playlist_song_data, headers, tablefmt="grid")
    print("List of Playlist Songs:")
    print(table)

@cli.command()
@click.option('--title', help='Filter songs by title')
def list_songs(title):
    songs = session.query(Song).all()

    if title:
        songs = [song for song in songs if title.lower() in song.song_title.lower()]

    song_data = [
        (song.song_id, song.song_title, song.album.album_title, song.artist.artist_name, song.genre.genre_name)
        for song in songs
    ]

    headers = ["Song ID", "Song Title", "Album Title", "Artist Name", "Genre Name"]

    table = tabulate(song_data, headers, tablefmt="grid")

    print("List of Songs:")
    print(table)


if __name__ == '__main__':
    cli()
