/* Provide a query that shows the total number of tracks in each playlist. The resultant table should include:
- Playlist name
- Total number of tracks on each playlist 
*/

SELECT Track.TrackId , COUNT(PlaylistTrack.TrackId), Playlist.Name FROM Track
JOIN PlaylistTrack ON Track.TrackId=PlaylistTrack.TrackId
JOIN Playlist ON PlaylistTrack.PlaylistId = Playlist.PlaylistId