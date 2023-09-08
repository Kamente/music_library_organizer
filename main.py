import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Playlist

DATABASE_URI = 'sqlite:///music.db'

engine = create_engine(DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    pass

@cli.command()
@click.argument('playlist_name')
def create_playlist(playlist_name):
    new_playlist = Playlist(playlist_name=playlist_name)
    session.add(new_playlist)
    session.commit()
    print(f'Playlist "{playlist_name}" created successfully.')

if __name__ == '__main__':
    cli()
