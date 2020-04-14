import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import silhouette_samples
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def clean_track_features(track_list):
    """Data cleaning and feature extraction of spotify tracks"""
    """
    Parameters
    ----------
    track_list : list of dictionaries
        Each dictionary is a track with features from functions.get_all_playlist_tracks()

    Returns
    -------
    df: pd.DataFrame
        Cleaned output ready for analysis
    """
    df = pd.DataFrame(track_list)
    df.drop_duplicates(subset='track_uri', inplace=True)
    # filter out tracks that are new and yet to have feature analysis
    df = df.loc[df['an_track_uri'] != -999]
    df = df.loc[df['an_track_uri'] != '-999']

    # --Feature extraction--

    # Dates
    df['release_year'] = df['release_date'].str.slice(stop=4)
    df['release_month'] = df['release_date'].str.slice(start=5, stop=7)
    df.loc[df['release_date_precision'] == 'year', 'release_month'] = -1 # na month where it's not given by spotify
    df.loc[df['release_date_precision'] == 'year', 'release_date'] = df['release_date'] + '-07-02' # When there's only a year, set to middle of the year
    df.loc[df['release_date_precision'] == 'month', 'release_date'] = df['release_date'] + '-15'  # When there's only a month and year, set to approx middle
    df['release_date'] = df['release_date'].astype('datetime64')
    df['days_since_release'] = (pd.to_datetime('today') - df['release_date']).dt.days
    df.drop(columns=['release_date', 'release_date_precision'], inplace=True)

    # Relative Popularity
    df['relpop_track_album'] = df['track_popularity'] - df['album_popularity']
    df['relpop_track_artist'] = df['track_popularity'] - df['artist_popularity']
    df['relpop_album_artist'] = df['album_popularity'] - df['artist_popularity']
    # Artist genres
    df.fillna(0, inplace=True)
    df['artist_jazz'] = df['artist_genres'].astype(str).str.contains('jazz')
    df['artist_pop'] = df['artist_genres'].astype(str).str.contains('pop')
    df['artist_indie'] = df['artist_genres'].astype(str).str.contains('indie')
    df['artist_rock'] = df['artist_genres'].astype(str).str.contains('rock')
    df['artist_electro'] = df['artist_genres'].astype(str).str.contains('electr|house|edm', regex=True)
    df['artist_randb'] = df['artist_genres'].astype(str).str.contains('r&b')
    df['artist_techno'] = df['artist_genres'].astype(str).str.contains('tech')
    df['artist_country'] = df['artist_genres'].astype(str).str.contains('country')
    df.drop(columns=['artist_genres', 'album_genres'], inplace=True)

    # Explicit
    df['explicit'] = df['explicit'].astype('str').str.lower().map({'true': 1, 'false': 0, 'unknown': 0})


    # Dropping other unnecessary columns
    df.drop(columns=['an_track_uri', 'an_album_uri', 'an_artist_uri'], inplace=True)

    return df.reset_index(drop=True)



def cluster_songs(songs_df):
    COLS = ['explicit', 'track_popularity', 'danceability','energy', 'key', 'loudness', 'mode', 'acousticness', 'instrumentalness',
    'liveness', 'valence', 'tempo', 'time_signature', 'release_year', 'release_month',
    'artist_jazz', 'artist_pop', 'artist_indie', 'artist_rock', 'artist_electro', 'artist_randb', 'artist_techno', 'artist_country']

    NO_SONGS = songs_df.shape[0]

    if NO_SONGS < 500:
        MIN_SONGS = int(NO_SONGS * 0.05)
    else:
        MIN_SONGS = 50


    anl_df = songs_df.loc[:, COLS]

    scaled_anl = StandardScaler().fit_transform(anl_df)

    best = {}
    best['score'] = -2

    for i in range(2, 10):
        km = KMeans(n_clusters=i, random_state=22)
        labels = km.fit_predict(scaled_anl)
        score = silhouette_score(scaled_anl, labels)

        if score > best['score']:
            best['score'] = score
            best['labels'] = labels
            best['no'] = i

        sample_scores = silhouette_samples(scaled_anl, best['labels'])


    songs_df['cluster'] = best['labels']
    songs_df['sample_score'] = sample_scores

    return songs_df



def plot_clusters(songs_df):
    COLS = ['explicit', 'track_popularity', 'album_total_tracks', 'artist_followers', 'artist_popularity',
    'album_popularity', 'danceability','energy', 'key', 'loudness', 'mode', 'acousticness', 'instrumentalness',
    'liveness', 'valence', 'tempo', 'time_signature', 'release_year', 'release_month', 'days_since_release',
    'relpop_track_album', 'relpop_track_artist', 'relpop_album_artist', 'artist_jazz', 'artist_pop', 'artist_indie',
    'artist_rock', 'artist_electro', 'artist_randb', 'artist_techno', 'artist_country']

    anl_df = songs_df.loc[:, COLS]

    pca = make_pipeline(StandardScaler(), PCA(n_components=2))
    x_pca = pca.fit_transform(anl_df)

    plt.figure(figsize=(30,30))
    plt.scatter(x_pca[:,0], x_pca[:,1], c=songs_df['cluster'], alpha=0.8)
    plt.savefig('temp-pca.png')
    plt.close()

    return


def get_pca_chart_vals(songs_df):
    COLS = ['explicit', 'track_popularity', 'album_total_tracks', 'artist_followers', 'artist_popularity',
    'album_popularity', 'danceability','energy', 'key', 'loudness', 'mode', 'acousticness', 'instrumentalness',
    'liveness', 'valence', 'tempo', 'time_signature', 'release_year', 'release_month', 'days_since_release',
    'relpop_track_album', 'relpop_track_artist', 'relpop_album_artist', 'artist_jazz', 'artist_pop', 'artist_indie',
    'artist_rock', 'artist_electro', 'artist_randb', 'artist_techno', 'artist_country']

    anl_df = songs_df.loc[:, COLS]

    pca = make_pipeline(StandardScaler(), PCA(n_components=2))
    x_pca = pca.fit_transform(anl_df)

    songs_df['PCA_1'] = x_pca[:,0]
    songs_df['PCA_2'] = x_pca[:,1]
    
    clust = songs_df['cluster'].unique()
    
    clust = pd.DataFrame(clust, columns=['cluster'])
    
    numb = len(clust)
    
    els = set_elements(numb)
    
    clust['pointStyle'] = els[0]
    clust['backgroundColor'] = els[1]
    
    songs_df = pd.merge(songs_df, clust, how='left', left_on='cluster', right_on='cluster', validate="m:1")
    songs_df = songs_df.loc[:, ['track_name', 'artist_name', 'pointStyle', 'backgroundColor', 'PCA_1', 'PCA_2', 'cluster']]
    
    
    clust_dict = {}
    
    for cluster in songs_df['cluster'].unique():
        tmp = songs_df.loc[songs_df['cluster'] == cluster]
        
        clust_dict[cluster] = {}
        clust_dict[cluster] = tmp.to_dict('r')
    
    return clust_dict





def get_ai_playlists(songs_df):
    """Function to convert clustering results DF to sorted playlists in dictionary format"""

    COLS = ['img', 'track_name', 'preview_url', 'artist_name']

    # We want to show the songs that have a preview URL first
    songs_df['has_preview'] = 1
    songs_df.loc[songs_df['preview_url'] == 0, 'has_preview'] = 0
    songs_df = songs_df.sort_values(by=['has_preview', 'sample_score'], ascending=False)

    ai_playlist = {}

    for cluster in songs_df['cluster'].unique():
        tmp = songs_df.loc[songs_df['cluster'] == cluster]

        avg_score = tmp['sample_score'].mean()
        no_tracks = tmp.shape[0]
        avg_pop = tmp['track_popularity'].mean()
        avg_year = int(tmp['release_year'].astype('int').mean())
        avg_energy = tmp['energy'].mean() * 100
        avg_dance = tmp['danceability'].mean() * 100
        avg_inst = tmp['instrumentalness'].mean() * 100
        avg_tempo = tmp['tempo'].mean()
        avg_happi = tmp['valence'].mean() * 100



        tmp = tmp.loc[:, COLS]

        ai_playlist[cluster] = {}
        ai_playlist[cluster]['description'] = {
            'avg_score': avg_score,
            'no_tracks': no_tracks,
            'avg_pop': avg_pop,
            'avg_energy': avg_energy,
            'avg_dance': avg_dance,
            'avg_inst': avg_inst,
            'avg_tempo': avg_tempo,
            'avg_happi': avg_happi,
        }
        ai_playlist[cluster]['songs'] = tmp.to_dict('r')

    return ai_playlist


def set_elements(no_clusters):
    """Function to define the pointStyle for chart.js based on number of clusters in total"""
    
    elements = ['circle', 'rect', 'triangle',  'star', 'crossRot', 'rectRounded', 'rectRot', 'dash', 'cross']
    cols = ['rgba(107,0,0, 0.7)', 'rgba(0,64,64, 0.7)', 'rgba(0,86,0, 0.7)','rgba(212,28,28, 0.7)',
           'rgba(17,127,127, 0.7)','rgba(22,169,22, 0.7)','rgba(212,111,28, 0.7)','rgba(9,140,9, 0.7)']
    
    all_elements = []
    all_cols = []
    
    j = 0
    for i in range(no_clusters):
        if (i % 8 == 0) & (j != 0):
            j = 0
            
        if len(all_elements) == no_clusters:
            break
        all_elements.append(elements[j])
        all_cols.append(cols[j])
        j += 1
    return all_elements, all_cols

