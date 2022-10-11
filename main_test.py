#!/usr/bin/env python
# coding: utf-8

# In[13]:


import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#constants - always should be placed at the top
Client_ID = ''
Client_Secret = ''

#url - https://www.billboard.com/charts/hot-100/# - where are you getting the information from???
url = 'https://www.billboard.com/charts/hot-100/'

#date - what date -for the week- do you want to get the chart from???
#date - how do we do that? - input function
#date - the format for the date has to be YYYY-MM-DD
#date - 1996-09-19 - the day I was born
date = input('Which year/month/day ➤ YYYY-MM-DD do you want to travel to?: ')

#requests.get(url, params={key: value}, args)
response = requests.get(f'{url}{date}')
response_html = response.text

#data - represents the document as a nested data structure
data = BeautifulSoup(response_html, 'html.parser')
class_data = 'c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only'
top_songs = data.find_all(name = 'h3', id = 'title-of-a-story', class_ = class_data)

#.strip() - removes any leading (spaces at the beginning) and trailing (spaces at the end) characters
top_100 = [song.get_text().strip() for song in top_songs]

#https://spotipy.readthedocs.io/en/2.19.0/# - spotipy documentation - must read!!! 
#note - need to read the documentation more to gain a better understanding of what it's asking
#1st guess - sp = spotipy.Spotify(auth_manager = SpotifyOAuth(parameters for the authentication manager))
sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        scope = 'playlist-modify-private',
        redirect_uri = 'https://example.com/callback/',
        client_id = Client_ID,
        client_secret = Client_Secret,
        show_dialog = True,
        cache_path = 'token.txt' 
    )
)
user_id = sp.current_user()['id']
#id - ''

#URIs - the resource identifier that you can enter, for example, in the Spotify Desktop client’s search box to locate an artist, album, or track
URIs = []

for songs in top_100:
    result = sp.search(q = f'track:{songs}')
    try:
        item = result['tracks']['items'][0]['uri']
        URIs.append(item)
    except:
        pass

playlist = sp.user_playlist_create(user = user_id, name = f'Billboard Hot 100 Playlist', public = False)
#we have to add tracks to the playlist - how do we do that??? - user_playlist_add_tracks(user, playlist_id, tracks, position = None)
sp.user_playlist_add_tracks(user = user_id, playlist_id = playlist['id'], tracks = URIs)

