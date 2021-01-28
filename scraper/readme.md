## Python Scraper

### Overview

This code is written in Python 3 for scraping flight emissions calculations from the ICAO
Carbon Emissions Calculator (ICEC). It requires the Selenium library for Python and the chromedriver by Google.
For a full requirements list, see the requirements.txt file in the main directory. 

The "PyScraper" class is used to control the browser and scrape the data.
The "functions.py" file contains all auxiliary functions used in the "run.py" file, including those to extract the unique trips and back-fill the remaining data after scraping the emissions calculations.
The "run.py" file runs the program using our flight logs dataset from BU. Please update the paths in this file according to your system. We recommend creating a scraper/data directory and housing your data.csv files there.