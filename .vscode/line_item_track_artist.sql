/* Provide a query that shows each Invoice line item, with the name of the track that was purchased, and the name of the artist.*/

SELECT InvoiceLine.InvoiceId, Track.Name, Album.ArtistId, Artist.Name  FROM InvoiceLine
JOIN Track ON InvoiceLine.TrackId = Track.TrackId
JOIN Album ON Track.AlbumId = Album.AlbumId
JOIN Artist ON Album.ArtistId = Artist.ArtistId
