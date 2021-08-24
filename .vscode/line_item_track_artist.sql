/* Provide a query that shows each Invoice line item, with the name of the track that was purchased, and the name of the artist.*/

SELECT
    iv.invoiceId InvoiceId,
    a.name ArtistName,
    t.name TrackName
FROM InvoiceLine iv
JOIN Album b ON b.AlbumId = t.AlbumId
JOIN Artist a ON a.ArtistId = b.ArtistId
JOIN Track t ON t.TrackId = iv.TrackId
