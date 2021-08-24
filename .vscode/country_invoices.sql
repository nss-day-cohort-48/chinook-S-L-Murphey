/*Provide a query that shows the total number of invoices per country.*/

SELECT COUNT(Invoice.InvoiceId), Invoice.BillingCountry FROM Invoice
GROUP BY Invoice.BillingCountry 
ORDER BY COUNT(Invoice.InvoiceId) DESC
