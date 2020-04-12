### Realistic Tomorrow
1. Correctly retrieve results from the form.
2. Add outline of the algorithm selection steps from sklearn.
3. Work out best way to put charts on the page
4. Skeleton Layout / thinking around this


### TODO 
***
1. Implement pause of audio when another song is played
5. Caching when reload of results page
1. Work out heuristic for grid of clusters to search over
2. Better genre feature engineering
5. Implement 3D Explorable chart of 3 component PCA, with explanation.
6. Give information about the playlists created
7. Save buttons for individual playlists, or all together?
8. Unit tests & integration tests
9. Deploy to digital ocean
10. Setup coverage checks & CI/CD from GitHub repository
11. Docker-ise
12. Change modal pop-up animation
13. Add favicon
4. Loading bar while POST is retrieving all Spotify Playlists
15. thank you / finished page



### IDEAS
-----------
1. You give your input songs, and then can select certain playlists you would like.
   1. i.e. "I want an upbeat playlist to dance too" -> It will select the relative most upbeat songs from your library
2. 


### Results Page Planning
-------------------------
- At the top, general explanation of the cluster
- Overview of how good the cluster split was with PCA graph (3D)
- General overview of their music taste
- Submit button for once they're done with their preference
- Each playlist is a collapsable card, with:
1. Playlist Number
2. Playlist Art Selected from Unsplash
2. Generated Playlist Name (Perhaps as form entry which you can edit) - would need controls
3. Number of tracks in playlist (small font)
4. Rough description of the songs in the playlist
5. Button on righthand side to include.


In the body:
General charts about the playlists (perhaps chartist.js?)
List of tracks to categories in the playlist
Play buttons for each (with pause when others are playing via jscript)
At the bottom, button to go back to top

