# employee-travel-emissions
We are working with two datasets: one which is collected automatically by the CONCUR booking platform, which all BU employees are required to use; and one which represents purchases made on the employee travel card, for example to cover a baggage fee or a taxi trip from the airport to a hotel, etc. 

## scrapers
This folder contains code for scraping websites. We test the technique first in Python and Selenium, and then move on to R for working with our data. See the corresponding subdirectories for more details. 

## clean
This folder contains a set of code for cleaning our data. In particular, we need to match entries in two different files by ticket number, and delete the duplicates. We are looking for unique trips not represented in the CONCUR data, but which manifest because of a purchase made on the travel card. 
