/*Provide a query that shows all the Tracks, but displays no IDs. The resultant table should include:
 - Album name
 - Media type
 - Genre
*/


SELECT 
    mt.Name mediaType,
    a.title albumTitle,
    g.name genre,
    t.name track
FROM Track t 
JOIN Album a ON t.AlbumId = a.AlbumId
JOIN MediaType mt ON t.MediaTypeId = mt.MediaTypeId
JOIN Genre g ON t.GenreId = g.GenreId