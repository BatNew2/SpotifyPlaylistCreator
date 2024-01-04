from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_SECRET_ID = os.environ.get("SPOTIPY_SECRET_ID")
SPOTIPY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI")
date = input("What date do you want to travel to? Type the date using this format DD-MM-YYYY: ").split("-")
print("Please wait...")
date = f"{date[2]}-{date[1]}-{date[0]}"
link = f"https://www.billboard.com/charts/hot-100/{date}"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="689c1abe9e7d425ba051cb66ef61305a",
        client_secret="1158d4e8ed0b416d94132c02cad9a455",
        show_dialog=True,
        cache_path="token.txt",
        username="J"
    )
)
user_id = sp.current_user()["id"]
try:
    response = requests.get(link)
    response.raise_for_status()
except requests.exceptions.HTTPError:
    print("Date invalid")
else:
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all(name="h3", id="title-of-a-story")
    titles = [title.get_text().replace("\n\n\t\n\t\n\t\t\n\t\t\t\t\t", "") for title in titles if titles.index(title) > 4]
    while len(titles) > 50:
        titles.pop(-1)
    titles = [title.replace("\t\t\n\t\n", "") for title in titles]
    formatted = [sp.search(q=song, limit=1, type="track", market=None) for song in titles]
    formatted = [song["tracks"]["items"][0]["id"] for song in formatted]
    print(formatted)
    playlist = sp.user_playlist_create(user=user_id, name=f"{date} playlist", public="false", description=f"Top songs from {date}\nSome songs may be inaccurate as the names are similar/the same")
    sp.playlist_add_items(playlist_id=playlist["id"], items=formatted, position=None)
    print(f"Finished, find playlist at {playlist['external_urls']['spotify']}")
