/*Looking at the InvoiceLine table, provide a query that COUNTs the number of line items for each Invoice.*/

SELECT InvoiceLine.InvoiceId, COUNT(*) AS "Line Items" FROM InvoiceLine
JOIN Invoice
ON InvoiceLine.InvoiceId = Invoice.InvoiceId
GROUP BY Invoice.InvoiceId
