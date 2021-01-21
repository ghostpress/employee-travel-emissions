This code is written in R for cleaning the Concur dataset. Among the changes:

1. Making a copy of the original .xsl data file to work in.
2. Sorting the data by year (according to departure date), and creating a new file for each.
3. Addressing invalid data points such as:
    - Those with "0" or empty value in the Distance column; or
    - Those with an empty value in the Ticket ID column.

   The invalid data will be extracted into a new file, in case it can be used later.
