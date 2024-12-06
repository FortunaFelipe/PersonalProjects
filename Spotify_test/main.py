import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests

#-----------------PART 1: Beautiful Soup---------------------#

date_choose = (input("pls enter the year u want (example ; 2002-01-17)"))
url =f"https://www.billboard.com/charts/hot-100/{date_choose}/"
session = requests.Session()
headers = {
'User-Agent': 'Mozilla/5.0',
'Referer': 'https://www.billboard.com/'
}
response = session.get(url=url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
#
# print(song_names)

#----------------------PART 2: SPOTIPY---------------------------#

CLIENT_ID = "CLIENTE ID"
CLIENT_PASS = "CLIENT PASSWORD"
YOUR_APP_REDIRECT_URI = "http://example.com"
redirect = "REDIRECT_URL"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_PASS,
                                               redirect_uri=YOUR_APP_REDIRECT_URI,
                                               scope="playlist-modify-private"))
user_id = sp.current_user()["id"]

song_uris = []
year = date_choose.split("-")[0]

for music in song_names:
    search = sp.search(q=f"track {music} year{year}", type="track")
    try:
        uri = search["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        print(uri)
    except IndexError:
        print(f"{music} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date_choose} Billboard 100", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

