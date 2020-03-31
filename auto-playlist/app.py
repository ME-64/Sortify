from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os

app = Flask(__name__)

client_id = 'b962565806ca4496996ae576320a957f'
client_secret = '1d61927e4edc401e91fa6b350c089c7b'
scope = 'user-read-email'
authorization_base_url = 'https://api.spotify.com/v1/authorize'
token_url = 'https://api.spotify.com/v1/api/token'

@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    spotify = OAuth2Session(client_id, scope=scope)
    authorization_url, state = spotify.authorization_url(authorization_base_url, {'client_id':
        client_id, 'client_secret': client_secret})

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    spotify = OAuth2Session(client_id, state=session['oauth_state'])
    token = spotify.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    return redirect(url_for('.profile'))


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    spotify = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(spotify.get('https://api.github.com/user').json())


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(debug=True)


