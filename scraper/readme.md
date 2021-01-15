## Python Scraper

### Overview

This code is written in Python 3 for scraping flight emissions calculations from the ICAO
Carbon Emissions Calculator (ICEC). It requires the Selenium library for Python and the chromedriver by Google.
For a full requirements list, see the requirements.txt file in the main directory. 

The "PyScraper" class is used to control the browser and scrape the data.
The "functions.py" file contains all auxiliary functions used in the "run.py" file, including those to extract the unique trips and back-fill the remaining data after scraping the emissions calculations.
The "run.py" file runs the program using our flight logs dataset from BU. Please update the paths in this file according to your system. We recommend creating a scraper/data directory and housing your data.csv files there.

### Use Instructions

Using the anaconda environment managing tool and our requirements.txt file, this work can be replicated in any machine. To do so, enter the following command in a terminal window:

`conda create --name myenv --file requirements.txt`

Where `myenv` is the name of your local environment.

After cloning this repository, you must download the chromedriver associated with your version of the browser. Check your version of Chrome [here](https://mdigi.tools/whatversion/) and then download the corresponding chromedriver .zip 
file for your OS and browser version [here](https://sites.google.com/a/chromium.org/chromedriver/downloads). Then place the unzipped chromedriver file in scraper/code and make it executable.