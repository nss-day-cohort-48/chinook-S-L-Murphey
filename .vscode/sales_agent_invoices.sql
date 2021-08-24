/* Provide a query that shows the invoices associated with each sales agent. The resultant table should include the Sales Agent's full name.*/

SELECT Invoice.InvoiceId, Employee.FirstName, Employee.LastName FROM Invoice
JOIN Customer ON Invoice.CustomerId = Customer.CustomerId
JOIN Employee ON Customer.SupportRepId = Employee.EmployeeId