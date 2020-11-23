# -*- coding: utf-8 -*-

# Set the working directory
import os
import sys
path = '/home/lucia/bu/sustainability/ccl/code/employee-travel-emissions/scrapers/Python/'  # edit according to system

os.chdir(path)
# print(os.getcwd()) - print test passed 11/18/20

# Import functions, settings, and data
sys.path.insert(0, './code')
from functions import*

scraper = Scraper()
scraper.openBrowser()  # must have chromedriver in Documents folder

# -----------------------------------------------------------------------------
# Some common methods

# Get the soup
soup = scraper.getSoup()

# Find all divs
divs = soup.find_all('div')

# Find a thing by a name
div = soup.find('div', {'id' : 'idName'})
div = soup.find('div', {'class' : 'className'})

