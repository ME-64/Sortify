import spotipy


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
               'album_total_tracks': song['track']['album']['total_tracks'],
               'img': song['track']['album']['images'][0]['url'],
               'track_name': song['track']['name'],
               'release_date': song['track']['album']['release_date'],
               'release_date_precision': song['track']['album']['release_date_precision'],
               'explicit': song['track']['explicit'],
               'track_popularity': song['track']['popularity'],
               'preview_url': song['track']['preview_url'],
               'artist_name': song['track']['artists'][0]['name'],
               'artist_uri': song['track']['artists'][0]['uri'],
               }
        tracks.append(tmp)

    while result['next']:
        result = spotify_object.next(result)
        for song in result['items']:
            tmp = {'track_uri': song['track']['uri'],
                   'album_uri': song['track']['album']['uri'],
                   'album_type': song['track']['album']['album_type'],
                   'album_name': song['track']['album']['name'],
                   'album_total_tracks': song['track']['album']['total_tracks'],
                   'img': song['track']['album']['images'][0]['url'],
                   'track_name': song['track']['name'],
                   'release_date': song['track']['album']['release_date'],
                   'release_date_precision': song['track']['album']['release_date_precision'],
                   'explicit': song['track']['explicit'],
                   'track_popularity': song['track']['popularity'],
                   'preview_url': song['track']['preview_url'],
                   'artist_name': song['track']['artists'][0]['name'],
                   'artist_uri': song['track']['artists'][0]['uri'],
                   }
            tracks.append(tmp)

    # --------------------
    # Getting audio analysis for each track
    track_ids = [x['track_uri'] for x in tracks]
    loops = int(len(track_ids) / 50)

    j = 0

    for i in range(0, loops):
        audio_features = spotify_object.audio_features(track_ids[i * 50:(i * 50) + 50])

        for features in audio_features:
            del features['track_href']
            del features['analysis_url']
            del features['type']
            del features['id']
            del features['duration_ms']
            features['an_track_uri'] = features.pop('uri')
            tracks[j].update(features)
            j += 1

    audio_features = spotify_object.audio_features(track_ids[loops * 50:])
    for features in audio_features:
        del features['track_href']
        del features['analysis_url']
        del features['type']
        del features['id']
        del features['duration_ms']
        features['an_track_uri'] = features.pop('uri')
        tracks[j].update(features)
        j += 1

    # -------------
    # Getting Album information for each track
    album_ids = [x['album_uri'] for x in tracks]
    loops = int(len(album_ids) / 20)
    j = 0
    for i in range(0, loops):
        album_features = spotify_object.albums(album_ids[i * 20:(i * 20) + 20])
        for features in album_features['albums']:
            tmp = {'album_genres': features['genres'],
                   'album_popularity': features['popularity'],
                   'an_album_uri': features['uri']}
            tracks[j].update(tmp)
            j += 1

    album_features = spotify_object.albums(album_ids[loops * 20:])
    for features in album_features['albums']:
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
            tmp = {'artist_followers': features['followers']['total'],
                   'artist_genres': features['genres'],
                   'an_artist_uri': features['uri'],
                   'artist_popularity': features['popularity']
                   }
            tracks[j].update(tmp)
            j += 1

    artist_features = spotify_object.artists(artist_ids[loops * 50:])
    for features in artist_features['artists']:
        tmp = {'artist_followers': features['followers']['total'],
               'artist_genres': features['genres'],
               'an_artist_uri': features['uri'],
               'artist_popularity': features['popularity']}
        tracks[j].update(tmp)
        j += 1

    return tracks
