This code is written in Python 3 for scraping data from websites. 
It contains a class, Scraper, that handles all of the browser navigation and getting content from the Selenium driver. 
It requires the selenium library for Python and the chromedriver by Google. 

Check your version of Chrome here (https://mdigi.tools/whatversion/) and then download the corresponding chromedriver .zip 
file for your OS and browser version here (https://sites.google.com/a/chromium.org/chromedriver/downloads). 
Place the unzipped chromedriver file in your Documents folder. Update the file path in Scraper as needed.

The "functions.py" file contains all other functions used to control the main scraper object. 
All content scraped from the scraper should be saved in the "./data" directory.

The "run.py" file runs the program to iteratively scrape a site.
