/*How many Invoices were there in 2009 and 2011?*/

SELECT COUNT(DISTINCT Invoice.InvoiceDate) FROM Invoice
WHERE InvoiceDate LIKE "%2009%" OR InvoiceDate LIKE "2011%"
