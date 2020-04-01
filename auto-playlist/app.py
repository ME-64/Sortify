from flask import Flask, request, redirect, session, url_for, render_template
from flask.json import jsonify
import json
import sqlite3
import os
import spotipy
import functions
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
import sys

CLIENT_ID = 'b962565806ca4496996ae576320a957f'
CLIENT_SECRET = '1d61927e4edc401e91fa6b350c089c7b'
SCOPE = 'user-library-read playlist-read-private playlist-modify-private'
USERNAME = '1120649038'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
AUTH_BASE_URI = 'https://accounts.spotify.com/authorize'
TOKEN_URI = 'https://accounts.spotify.com/api/token'
USER_API = 'https://api.spotify.com/v1/me'

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
    playlists = functions.get_user_playlists(sp)
    playlists = playlists[0:5]
    for playlist in playlists:
        if len(playlist['name']) >40:
            playlist['name'] = playlist['name'][0:37] + '...'

    playlists = [playlist for playlist in playlists if playlist['tracks'] > 0]
        

    user = 'milo'
    library_tracks = 231
    return render_template('selection.html', playlists=playlists, user=user, library_tracks=library_tracks)


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        checks = request.form.getlist('checks')
        session['checks'] = checks.copy()

    sp = spotipy.Spotify(auth=session['token']['access_token']) 

    tracks = []

    library = functions.get_playlist_tracks('library', sp)
    tracks.extend(library)

    for playlist in checks:
        tmp = functions.get_playlist_tracks(playlist, sp)
        tracks.extend(tmp)

    return jsonify(tracks)



if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.secret_key = os.urandom(24)
    app.run(debug=True)
