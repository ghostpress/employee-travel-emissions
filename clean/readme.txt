This code is written in Python for cleaning the Concur dataset. Among the operations:

1. Deleting rows with values of 0 in the Distance (miles) column, or in which the departure and arrival airport codes are the same.
2. Deleting rows in the data with values of None in the Ticket ID column.
3. Creating new columns for the Departure Month and Departure Year, from the Departure Date column.
