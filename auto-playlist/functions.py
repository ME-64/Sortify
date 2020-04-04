import spotipy

def get_user_playlists(spotify_object):
    """Function to get all of a users playlists"""
    result = spotify_object.current_user_playlists()
    playlists = []
    for p in result['items']:
        tmp = {
            'playlist_uri': p['uri'],
            'name': p['name'],
            'desc': p['description'],
            'img': p['images'][0]['url'] if len(p['images']) > 0 else None,
            'color': p['primary_color'],
            'tracks': p['tracks']['total']
        }
        playlists.append(tmp)


    while result['next']:
        result = spotify_object.next(result)
        for p in result['items']:
            tmp = {
                'playlist_uri': p['uri'],
                'name': p['name'],
                'desc': p['description'],
                'img': p['images'][0]['url'] if len(p['images']) > 0 else None,
                'color': p['primary_color'],
                'tracks': p['tracks']['total']
            }
            playlists.append(tmp)
    playlists = sorted(playlists, key=lambda i: i['tracks'], reverse=True)
    return playlists



def get_playlist_tracks(playlist_id, spotify_object):
    """Function to get information about all the tracks in a playlist"""
    if playlist_id == 'library':
        result = spotify_object.current_user_saved_tracks()
    else:
        result = spotify_object.playlist_tracks(playlist_id=playlist_id)

    tracks = []

    for song in result['items']:
        tmp = {'track_uri': song['track']['uri'],
               'album_uri': song['track']['album']['uri'],
               'album_type': song['track']['album']['album_type'],
               'album_name': song['track']['album']['name'],
               'img': song['track']['album']['images'][0]['url'] if len(song['track']['album']['images']) > 0 else None,
               'track_name': song['track']['name'],
               'release_date': song['track']['album']['release_date'],
               'release_date_precision': song['track']['album']['release_date_precision'],
               'explicit': song['track']['explicit'],
               'track_popularity': song['track']['popularity'],
               'preview_url': song['track']['preview_url'],
               'artist_name': song['track']['artists'][0]['name'],
               'artist_uri': song['track']['artists'][0]['uri'],
               }
        try:
            tmp['album_total_tracks'] = song['track']['album']['total_tracks']
        except:
            tmp['album_total_tracks'] = 1
        
        tracks.append(tmp)

    while result['next']:
        result = spotify_object.next(result)
        for song in result['items']:
            tmp = {'track_uri': song['track']['uri'],
                   'album_uri': song['track']['album']['uri'],
                   'album_type': song['track']['album']['album_type'],
                   'album_name': song['track']['album']['name'],
                   'img': song['track']['album']['images'][0]['url'] if len(song['track']['album']['images']) > 0 else None,
                   'track_name': song['track']['name'],
                   'release_date': song['track']['album']['release_date'],
                   'release_date_precision': song['track']['album']['release_date_precision'],
                   'explicit': song['track']['explicit'],
                   'track_popularity': song['track']['popularity'],
                   'preview_url': song['track']['preview_url'],
                   'artist_name': song['track']['artists'][0]['name'],
                   'artist_uri': song['track']['artists'][0]['uri'],
                   }
            try:
                tmp['album_total_tracks'] = song['track']['album']['total_tracks']
            except:
                tmp['album_total_tracks'] = 1
            
            tracks.append(tmp)
            
    tracks = [track for track in tracks if track['track_uri'][8:13] not in ['local', 'episo']]

    # --------------------
    # Getting audio analysis for each track
    track_ids = [x['track_uri'] for x in tracks]
    loops = int(len(track_ids) / 50)

    j = 0

    for i in range(0, loops):
        audio_features = spotify_object.audio_features(track_ids[i * 50:(i * 50) + 50])
        for features in audio_features:
            if j != len(track_ids):
                features.pop('track_href', None)
                features.pop('analysis_url', None)
                features.pop('type', None)
                features.pop('id', None)
                features.pop('duration_ms', None)
                features['an_track_uri'] = features.pop('uri')
                tracks[j].update(features)
                j += 1
                
    if j-1 != len(track_ids):
        audio_features = spotify_object.audio_features(track_ids[j:])
        for features in audio_features:
            if j != len(track_ids):
                features.pop('track_href', None)
                features.pop('analysis_url', None)
                features.pop('type', None)
                features.pop('id', None)
                features.pop('duration_ms', None)
                features['an_track_uri'] = features.pop('uri')
                tracks[j].update(features)
                j += 1

    # -------------
    # Getting Album information for each track
    album_ids = [x['album_uri'] for x in tracks]
    loops = int(len(album_ids) / 20)
    j = 0
    for i in range(0, loops):
        if j != len(album_ids):
            album_features = spotify_object.albums(album_ids[i * 20:(i * 20) + 20])
            for features in album_features['albums']:
                if j != len(album_ids):
                    tmp = {'album_genres': features['genres'],
                           'album_popularity': features['popularity'],
                           'an_album_uri': features['uri']}
                    tracks[j].update(tmp)
                    j += 1

    if j-1 != len(album_ids):
        album_features = spotify_object.albums(album_ids[j:])
        for features in album_features['albums']:
            if j != len(album_ids):
                tmp = {'album_genres': features['genres'],
                       'album_popularity': features['popularity'],
                       'an_album_uri': features['uri']}
                tracks[j].update(tmp)
                j += 1

    # -----------
    # Getting Artist information for each track
    artist_ids = [x['artist_uri'] for x in tracks]
    loops = int(len(album_ids) / 50)
    j = 0
    for i in range(0, loops):
        artist_features = spotify_object.artists(artist_ids[i * 50:(i * 50) + 50])
        for features in artist_features['artists']:
            if j != len(artist_ids):
                tmp = {'artist_followers': features['followers']['total'],
                       'artist_genres': features['genres'],
                       'an_artist_uri': features['uri'],
                       'artist_popularity': features['popularity']
                       }
                tracks[j].update(tmp)
                j += 1

    if j-1 != len(artist_ids):
        artist_features = spotify_object.artists(artist_ids[j:])
        for features in artist_features['artists']:
            if j != len(artist_ids):
                tmp = {'artist_followers': features['followers']['total'],
                       'artist_genres': features['genres'],
                       'an_artist_uri': features['uri'],
                       'artist_popularity': features['popularity']}
                tracks[j].update(tmp)
                j += 1

    return tracks