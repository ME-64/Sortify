import json
import os
import sqlite3
import sys

import requests
import spotipy
from flask import Flask, redirect, render_template, request, session, url_for
from flask.json import jsonify
from oauthlib.oauth2 import WebApplicationClient

import functions2
import analysis

from dotenv import load_dotenv
load_dotenv(override=True)
CLIENT_ID = os.environ['spotipy_client_id']
CLIENT_SECRET = os.environ['spotipy_client_secret']
SCOPE = 'user-library-read playlist-read-private playlist-modify-private user-read-private'
USERNAME = '1120649038'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
AUTH_BASE_URI = 'https://accounts.spotify.com/authorize'
TOKEN_URI = 'https://accounts.spotify.com/api/token'
USER_API = 'https://api.spotify.com/v1/me'


# Patching spotipy

setattr(spotipy.Spotify, 'current_user_saved_tracks', functions2.current_user_saved_tracks)


# app setup
app = Flask(__name__, static_folder='templates/static/')

# client setup
client = WebApplicationClient(client_id=CLIENT_ID)


@app.route("/")
def index():
    return render_template('home.html')


@app.route("/login")
def login():
    # Find out what URL to hit for Google login

    request_uri = client.prepare_request_uri(
        AUTH_BASE_URI,
        redirect_uri=request.base_url + "/callback",
        scope=SCOPE,
        show_dialog=True
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        TOKEN_URI,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(CLIENT_ID, CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    session['token'] = client.token

    return redirect(url_for('selection'))


@app.route('/selection', methods=['GET'])
def selection():
    sp = spotipy.Spotify(auth=session['token']['access_token'])
    playlists = functions2.get_user_playlists(sp)
    playlists = playlists[0:]
    for playlist in playlists:
        if len(playlist['name']) >20:
            playlist['name'] = playlist['name'][0:17] + '...'

        if len(playlist['desc']) > 80:
            playlist['desc'] = playlist['desc'][0:78] + '...'

    playlists = [playlist for playlist in playlists if playlist['tracks'] > 0]


    details = functions2.get_user_information(sp)

    user = details['name']

    if user == '1120649038':
        user = 'Milo'

    img = details['image']
    session['country'] = details['country']

    library_tracks = 231
    return render_template('selection_new.html', playlists=playlists, user=user, library_tracks=library_tracks, img=img)


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        checks = request.form.getlist('checks')
        session['checks'] = checks.copy()
        print(checks,flush=True)
        sp = spotipy.Spotify(auth=session['token']['access_token'])

        tracks = []

        library = functions2.get_all_track_features_from_playlists('library', sp, session['country'])
        tracks.extend(library)

        if len(checks) > 0:
            tmp = functions2.get_all_track_features_from_playlists(checks, sp, session['country'])
            tracks.extend(tmp)

        clean_tracks = analysis.clean_track_features(tracks)
        clustered_tracks = analysis.cluster_songs(clean_tracks)
        analysis.plot_clusters(clustered_tracks)

        no_clusters = clustered_tracks['cluster'].nunique()

        ai_playlists = analysis.get_ai_playlists(clustered_tracks)


    return render_template('results_new.html')# no_clusters=no_clusters, ai_playlists=ai_playlists)



if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.secret_key = os.urandom(24)
    app.run(debug=True, host='0.0.0.0')
