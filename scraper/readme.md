## Python Scraper

### Overview

This code is written in Python 3 for scraping flight emissions calculations from the ICAO
Carbon Emissions Calculator. It requires the Selenium library for Python and the chromedriver by Google.
For a full requirements list, see the requirements.txt file (coming soon). 

The "functions.py" file contains all functions used to control the browser and scrape the data. 
The "run.py" file runs the program using our flight logs dataset from BU.

### Use Instructions

Check your version of Chrome [here](https://mdigi.tools/whatversion/) and then download the corresponding chromedriver .zip 
file for your OS and browser version [here](https://sites.google.com/a/chromium.org/chromedriver/downloads). 
Place the unzipped chromedriver file in your Documents folder and make it executable. Update the file path in functions.py as needed.

Using the anaconda environment managing tool and our requirements.txt file (coming soon), this work can be replicated in any machine. 
To do so, enter the following command in a terminal window:

`conda create --name myenv --file requirements.txt`

Where `myenv` is the name of your local environment.