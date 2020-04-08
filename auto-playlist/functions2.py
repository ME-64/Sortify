import re

def current_user_saved_tracks(self, limit=20, offset=0, market=None):
    """Patch to allow spotipy to specify market for user's library"""
    return self._get("me/tracks", limit=limit, offset=offset, market=market)


def get_user_information(spotify_object):
    """Function to get information about the currently logged in Spotify User"""
    result = spotify_object.current_user()
    details = {}

    if result['display_name'].isnumeric():
        details['name'] = result['display_name']
    else:
        details['name'] = result['display_name'].split(' ')[0] + ', '

    if len(result['images']) > 0:
        details['image'] = result['images'][2]['url'] 
    else:
        details['image'] = 'https://www.gravatar.com/avatar/?d=mm' # stock user image
        # details['image'] = None

    details['country'] = result['country']

    return details
    

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
    # Not using sorting functionality for now
    # playlists = sorted(playlists, key=lambda i: i['tracks'], reverse=True)
    playlists = [playlist for playlist in playlists if playlist['tracks'] > 1]
    
    for playlist in playlists:
        playlist['desc'] = remove_html_tags(playlist['desc'])
    return playlists



def get_playlist_tracks(playlist_ids, spotify_object, market=None):
    """Function to get information about all the tracks in a playlist"""
    tracks = []
    if isinstance(playlist_ids, str):
        playlist_ids = [playlist_ids]
    
    for playlist_id in playlist_ids:
        # print(f'going through {playlist_id}')
        if playlist_id == 'library':
            result = spotify_object.current_user_saved_tracks(market=market)
        else:
            result = spotify_object.playlist_tracks(playlist_id=playlist_id, market=market)


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
        # print(f'gone through {playlist_id}')
        
#     for track in tracks:
#         if track['track_uri'][8:13] == 'local':
#             print('removing LOCAL track')
    tracks = [track for track in tracks if track['track_uri'][8:13] not in ['local', 'episo']]

    return tracks


    
def get_albums_features(album_ids, spotify_object):
    # import pdb; pdb.set_trace()
    if isinstance(album_ids, str):
        raise TypeError
    
    albums = []
    loops = int(len(album_ids) / 20) #1
    j = 0
    for i in range(0, loops): # 0 - 1
        album_features = spotify_object.albums(album_ids[i * 20:(i * 20) + 20]) # first 20
        for features in album_features['albums']:
            tmp = {'album_genres': features['genres'],
                   'album_popularity': features['popularity'],
                   'an_album_uri': features['uri']}
            albums.append(tmp)
            j += 1

    if loops != len(album_ids) / 20:
        album_features = spotify_object.albums(album_ids[j:])
        for features in album_features['albums']:
            tmp = {'album_genres': features['genres'],
                   'album_popularity': features['popularity'],
                   'an_album_uri': features['uri']}
            albums.append(tmp)
            j += 1
        
    return albums
        
                
        


def get_artists_features(artist_ids, spotify_object):
    # import pdb; pdb.set_trace()
    if isinstance(artist_ids, str):
        raise TypeError
    
    artists = []
    loops = int(len(artist_ids) / 50) #1
    j = 0
    for i in range(0, loops): # 0 - 1
        artist_features = spotify_object.artists(artist_ids[i * 50:(i * 50) + 50]) # first 20
        for features in artist_features['artists']:
            tmp = {'artist_followers': features['followers']['total'],
                   'artist_genres': features['genres'],
                   'an_artist_uri': features['uri'],
                   'artist_popularity': features['popularity']
                   }
            artists.append(tmp)
            j += 1

    if loops != len(artist_ids) / 50:
        artist_features = spotify_object.artists(artist_ids[j:])
        for features in artist_features['artists']:
            tmp = {'artist_followers': features['followers']['total'],
                   'artist_genres': features['genres'],
                   'an_artist_uri': features['uri'],
                   'artist_popularity': features['popularity']
                   }
            artists.append(tmp)
            j += 1
        
    return artists



def get_tracks_features(track_ids, spotify_object):
    # import pdb; pdb.set_trace()
    if isinstance(track_ids, str):
        raise TypeError
    
    tracks = []
    loops = int(len(track_ids) / 50) #1
    j = 0
    for i in range(0, loops): # 0 - 1
        track_features = spotify_object.audio_features(track_ids[i * 50:(i * 50) + 50]) # first 20
        for features in track_features:
            if features is not None:
                tmp = {
                    'danceability': features['danceability'],
                    'energy': features['energy'],
                    'key': features['key'],
                    'loudness': features['loudness'],
                    'mode': features['mode'],
                    'acousticness': features['acousticness'],
                    'instrumentalness': features['instrumentalness'],
                    'liveness': features['liveness'],
                    'valence': features['valence'],
                    'tempo': features['tempo'],
                    'time_signature': features['time_signature'],
                    'an_track_uri': features['uri']
                }
                
            else:
                tmp = {
                    'danceability': -999,
                    'energy': -999,
                    'key': -999,
                    'loudness': -999,
                    'mode': -999,
                    'acousticness': -999,
                    'instrumentalness': -999,
                    'liveness': -999,
                    'valence': -999,
                    'tempo': -999,
                    'time_signature': -999,
                    'an_track_uri': -999
                } 
            tracks.append(tmp)
            j += 1

    if loops != len(track_ids) / 50:
        track_features = spotify_object.audio_features(track_ids[j:])
        for features in track_features:
            if features is not None:
                tmp = {
                    'danceability': features['danceability'],
                    'energy': features['energy'],
                    'key': features['key'],
                    'loudness': features['loudness'],
                    'mode': features['mode'],
                    'acousticness': features['acousticness'],
                    'instrumentalness': features['instrumentalness'],
                    'liveness': features['liveness'],
                    'valence': features['valence'],
                    'tempo': features['tempo'],
                    'time_signature': features['time_signature'],
                    'an_track_uri': features['uri']
                }
                
            else:
                tmp = {
                    'danceability': -999,
                    'energy': -999,
                    'key': -999,
                    'loudness': -999,
                    'mode': -999,
                    'acousticness': -999,
                    'instrumentalness': -999,
                    'liveness': -999,
                    'valence': -999,
                    'tempo': -999,
                    'time_signature': -999,
                    'an_track_uri': -999
                } 
            tracks.append(tmp)
            j += 1
        
    return tracks
    


def get_all_track_features_from_playlists(playlist_ids, spotify_object, market=None):
    
    tracks = get_playlist_tracks(playlist_ids, spotify_object, market=market)
    tracks = [track for track in tracks if track['track_uri'][8:13] != 'local']
    
    track_ids = [x['track_uri'] for x in tracks]
    album_ids = [x['album_uri'] for x in tracks]
    artist_ids = [x['artist_uri'] for x in tracks]
    
    track_features = get_tracks_features(track_ids, spotify_object)
    artist_features = get_artists_features(artist_ids, spotify_object)
    album_features = get_albums_features(album_ids, spotify_object)
    
    for track, artist, album, track_more in zip(tracks, artist_features, album_features, track_features):
        track.update(artist)
        track.update(album)
        track.update(track_more)
        
    return tracks

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

