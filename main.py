from pathlib import Path
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import requests
import spotipy
import os

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

ask_year_songs = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{ask_year_songs}/")
list_songs = response.text

soup = BeautifulSoup(list_songs, "html.parser")
list_music_top_1 = soup.find_all(name="h3", id="title-of-a-story", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet")
list_music_99 = soup.find_all(name="h3", id="title-of-a-story", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")

name_songs_top_1 = [song.getText().strip("\n") for song in list_music_top_1]
name_songs_99_name = [song.getText().strip("\n") for song in list_music_99]

for i in name_songs_99_name:
    name_songs_top_1.append(i)

mix_name_songs = name_songs_top_1

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/callback/",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
song_uris = []

year = str(ask_year_songs).split("-")[0]

for song in mix_name_songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track") 

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
        pass

playlist = sp.user_playlist_create(user=user_id, name=f"{ask_year_songs} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


