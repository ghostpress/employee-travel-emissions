# Import Libraries

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from scrapers.Python.code.chromedriver import chrome_driver

link = 'https://applications.icao.int/icec'

# Initiate the driver, load web elements into BeautifulSoup

driver = chrome_driver(link)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

departure_input = driver.find_element_by_name('frm1')          # Get input for the departure field
departure_airport = input("What is your departure airport? ")  # TODO: automate to read from dataset
print("Your airport of departure is: ", departure_airport)     # print test passed 12/22/20







# Set the working directory
import os
import sys
# path = '/home/lucia/bu/sustainability/ccl/code/employee-travel-emissions/scrapers/Python/'  # edit according to system

# os.chdir(path)

# Import functions, settings, and data
# sys.path.insert(0, './code')
# from functions import*

# scraper = Scraper()
# scraper.openBrowser()  # must have chromedriver in Documents folder

# scraper.createFolder('data')  # run only once TODO: make cleaner
# scraper.screenshot('./data/temp.png')

# -----------------------------------------------------------------------------
# Some common methods

# Get the soup
# soup = scraper.getSoup('html')

# Find all divs
# divs = soup.find_all('div')

# Find a thing by a name
# div = soup.find('div', {'id' : 'idName'})
# div = soup.find('div', {'class' : 'className'})

# Close the session
# scraper.quitBrowser()

