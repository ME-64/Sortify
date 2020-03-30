import os
from flask import Flask, render_template, redirect, url_for, g
import spotipy

client_id = os.environ['spotipy_client_id']
client_secret = os.environ['spotipy_client_secret']
username = '1120649038'
scope = 'user-library-read'


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, world!'

    @app.route('/')
    def home():
        return render_template('home.html')


    @app.route('/auth')
    def authorise():
        token = spotipy.util.prompt_for_user_token(
            username=username, scope=scope,
            client_id=client_id, client_secret=client_secret,
            redirect_uri='http://127.0.0.1:5000/auth/success')


    @app.route('/auth/<code>')
    def is_auth(code):
        if code is not None:
            g.code = code
            return render_template('success.html')
        else:
            return redirect(url_for('/'))

    return app