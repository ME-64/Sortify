import pandas as pd
import numpy as np
import spotipy
import os
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import silhouette_samples
from sklearn.decomposition import PCA

import functions2
import analysis


CLIENT_ID = os.environ['spotipy_client_id']
CLIENT_SECRET = os.environ['spotipy_client_secret']
SCOPE = 'user-library-read playlist-read-private playlist-modify-private user-read-private'
USERNAME = '1120649038'


client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


setattr(spotipy.Spotify, 'current_user_saved_tracks', functions2.current_user_saved_tracks)


songs = functions2.get_all_track_features_from_playlists('spotify:playlist:37i9dQZF1DX9uKNf5jGX6m',sp, 'GB')

clean_tracks = analysis.clean_track_features(songs)
clustered_tracks = analysis.cluster_songs(clean_tracks)


COLS = ['explicit', 'track_popularity', 'album_total_tracks', 'artist_followers', 'artist_popularity',
'album_popularity', 'danceability','energy', 'key', 'loudness', 'mode', 'acousticness', 'instrumentalness',
'liveness', 'valence', 'tempo', 'time_signature', 'release_year', 'release_month', 'days_since_release',
'relpop_track_album', 'relpop_track_artist', 'relpop_album_artist', 'artist_jazz', 'artist_pop', 'artist_indie',
'artist_rock', 'artist_electro', 'artist_randb', 'artist_techno', 'artist_country']

anl_df = clustered_tracks.loc[:, COLS]

pca = make_pipeline(StandardScaler(), PCA(n_components=2))
x_pca = pca.fit_transform(anl_df)


clustered_tracks['PCA_1'] = x_pca[:,0]
clustered_tracks['PCA_2'] = x_pca[:,1]

clustered_tracks.head()



