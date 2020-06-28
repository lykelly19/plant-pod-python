#!/usr/bin/env python
from flask import Flask, flash, redirect, render_template, request, url_for
import sys
import spotify
import requests
import json

app = Flask(__name__)

def getSpotifyTrack(track_name):
    AUTH_URL = ""
    CLIENT_ID = ""
    CLIENT_SECRET = ""

    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    auth_response_data = auth_response.json()
    SPOTIFY_ACCESS_TOKEN = auth_response_data['access_token']

    headers = { 'Authorization': 'Bearer {token}'.format(token=SPOTIFY_ACCESS_TOKEN) }
    BASE_URL = 'https://api.spotify.com/v1/'

    artist_name = 'the-beatles'

    track = requests.get(BASE_URL + 'search?q=' + track_name + '%20artist:' + artist_name + '&type=track&limit=1', headers=headers)
    track = track.json()

    track_uri = track['tracks']['items'][0]['uri'].replace('spotify:track:', '')

    audio_features = requests.get(BASE_URL + 'audio-features/' + track_uri, headers=headers)
    audio_features = audio_features.json()

    # 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'liveness', 'tempo'
    return audio_features['danceability']


@app.route('/')
def index():

    with open('beatles-songs.json') as json_file:
        songs_name = json.load(json_file)

    return render_template(
        'index.html',
        data=songs_name['songs'])


@app.route("/test" , methods=['GET', 'POST'])
def test():
    select = request.form.get('comp_select')

    track_name = select.lower().replace(' ', '-')
    danceability = getSpotifyTrack(track_name)

    return(str(select) + str(danceability)) 


if __name__=='__main__':
    app.run(debug=True)
