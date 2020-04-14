# Sortify - Automatically sort your spotify music
--------------------------------------------
*Sorify utilises unsupervised machine learning techniques to sort your music library for you*

### Todo Per Page
----------------
**Home Page**
- [ ] Fix spacing for mobile displays
- [ ] Fix NAV Bar to show meaningful links
- [ ] Fix NAV Bar 'burger' moving on mobile to the side
- [ ] Fix vertical spacing of links at bottom on mobile
- [X] Remove hyphen from the name
- [ ] Change name of app on Spotify to reflect true name.
- [ ] Change order of asked for user scopes (Maybe remove user-read-private?)

**Selection Page**
- [ ] Center 1,2,3 stages on mobile ("select songs goes to two lines currently")
- [ ] Increase padding on scrollable list to make it easier to circumnavigate
- [ ] Make the song names "..." change with the width of the container
- [ ] Add the real user image where applicable to the leftside of title bar.
- [ ] Add a description of the limitations on min and max songs
- [ ] Give them the option to include / exclude their library
- [ ] *Tweaks Section*
  - [ ] Give them the option to sprinkle in additional songs we think they might like
  - [ ] Change various attributes of the sort (?) Min/Max Playlist size
  - [ ] "Advanced user" option to select the sorting algorithm
- [ ] *Get Results*
  - [ ] Make the button cleaner to look at
  - [ ] Give them a progress bar as the button loads
  - [ ] Give them the count of the number of songs currently selected

**Results Page**
- [ ] Remove user icon on small screen viewport
- [ ] "We found X unique playlists from your music collection"
- [ ] Section at the top describing overall trends about someone's music library
- [ ] *Top Charts*
    - [ ] Remove cross and start from element selection.
    - [ ] Mix up the colour - element combination, rather than linear
    - [ ] Add breakdown by Artist Genre Pie Chart
    - [ ] Add total song count
    - [ ] Add most included genre
- [ ] Chart showing the seperation of the songs into the playlists (3D perhaps?)
- [ ] Playlist Name better format, and as an input box that can be changed
- [ ] songs moved to the left and with general attributes about playlist
- [ ] Include button goes to TICK or CROSS
- [ ] Better play / pause button and stop when other one is played / paused.
- [ ] *Per Playlist*
   - [ ] Attributes describing the playlist

**Done Page**
- [ ] Thanks for using Sortify, feedback, restart etc


**FAQ Page**
- [ ] tbd

**About Page**
- [ ] tbd

**Backend Work**
- [ ] Load library on selection page for count of songs
- [ ] Store a database of songs and their attributes for added similiarity?
- [ ] Filter out playlists that aren't good enough
- [ ] Compute general attributes about their music libraries
- [ ] Generate playlist names based on the songs in the library
- [ ] Generate playlist album covers from sortify
- [ ] Database for event logging
- [ ] Continous Integration / Deployment setup
- [ ] Bonus year seperation playlist (?)
- [ ] Dockerise the project
- [ ] Better genre feature engineering
- [ ] Caching of results on final page

**General Flask**
- [ ] Handling of errors when not authenticated
- [ ] Tests
- [ ] Favicon

**General Github**
- [ ] Change repository name




# Spotify Features Dictionary
-------------------------------
##### From the Audio Feature Endpoint
`duration_ms`: Duration of the track in milliseconds

`key`: Estimated overall key of the track. Integers map to pitches using Pitch Class
Notation. If no key is detected then the value is -1

`mode`: Indicates the modality (major / minor) of a track. The types scale from which
melodic content is derived. Major is represented by 1 and minor is 0

`time_signature`: An estimated overall time signature of a track. The time signature
(meter) is a notational convention to specify how many beats are in each bar or measure

`acousticness`: A confidence measure from 0-1 of whether a track is acoustic. Most tracks
are close to 0 for this feature

`danceability`: Describes how suited a track is to dance to (based on tempo, rhythm 
stability, beat strength, & overall regularity). Ranges between 0-1, 0 being least 
danceable. Features are roughly normally distributed

`energy`: Measure from 0-1 that represents intensity & activity. Energetic tracks are
fast, loud & noisy.

`instrumentalness`: Predicts whether a track contains no vocals. Closer to 1 = 
more likely to be instrumental. Values above 0.5 are intended to represent instrumental
tracks. Most values are close to 0, with the rest being 0.8-1

`liveness`: detects the presence of an audience in the recording. Higher values mean
more likely it was live. 0.8+ means strong likelihood a song is live

`loudness`: Overall loudness of a sound averaged across the entire track and are useful
for comparing the relative loudness of a track. Loudness is the quality of a sound that
is the primary psychological correlate of physical strength (amplitude). Values range
between -60 and 0 db.

`Speechiness`: Speechiness detects the presence of spoken words in a track. The closer
the track is to a talk show/radio/etc the closer to 1.0. Values above 0.66 describe 
tracks that are probably made entirely of spoken words

`Valence`: A measure from 0 to 1 describing musical positiveness of a track. Tracks 
with high valence sound more happy/cheerful/euphoric, while tracks with low valence
sound more sad/depressed/angry.

`tempo`: Overall estimated tempo of a track in BPM.

##### From the Get Track Endpoint
 `explicit`: True/False/Unknown

 `popularity`: Measure from 0 to 100. Based mostly on the total number of plays a
 track gets, and how recent they were. Lags true popularity by a few days
 
 
##### From the Artists Endpoint
`followers`: Total number of followers on the platform

`genres`: Array of strings with the genres the artist is associated with

`popularity`: Based on the popularity of all the artists tracks


##### From the Albums Endpoint

`genres`: Array of strings with the genres the artist is associated with

`release_data`: date which the album was released. Depending on precision could either
be YYYY-MM-DD, YYYY-MM, or YYYY.

`popularity`: Popularity derived from the popularity of the songs in the album.

