# Import Libraries

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import time
import pandas as pd

from scrapers.Python.code.chromedriver import chrome_driver

link = 'https://applications.icao.int/icec'

# Initiate the driver, load web elements into BeautifulSoup

driver = chrome_driver(link)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

departure_input = driver.find_element_by_name('frm1')          # Get input for the departure field
print(type(departure_input))
departure_airport = input("What is your departure airport? ")  # TODO: automate to read from dataset
print("Your airport of departure is: ", departure_airport)     # print test passed 12/22/20

# Send departure info to ICAO calculator

departure_input.send_keys(departure_airport)
departure_click_wait = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "/html/body/ul[1]")))
departure_items = departure_click_wait.find_elements_by_tag_name("li")

# Print options from the drop-down menu, click the correct one
# print test passed 12/23/20

for index in range(len(departure_items)):
    text = (departure_items[index]).text
    print("-------")
    print(text)

if len(departure_items) == 1:
    departure_index = '1'
else:
    departure_index = input("Which of the options is your correct departure airport code?\n"
                            "Enter 1 for first, 2 for second, etc. ")

departure_element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "/html/body/ul[1]/li[" + departure_index + "]")))
departure_element.click()  # test passed 12/23/20

destination_input = driver.find_element_by_name("to1")             # Get input for the destination field
destination_airport = input("What is your destination airport? ")  # TODO: automate to read from dataset
print("Your airport of destination is: ", destination_airport)     # print test passed 12/23/20

# Send destination info to ICAO

destination_input.send_keys(destination_airport)
time.sleep(2)

destination_click_wait = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "/html/body/ul[2]")))
destination_items = destination_click_wait.find_elements_by_tag_name("li")

# Print items from the drop-down menu, click the correct one
# print test passed 12/23/20

for index in range(len(destination_items)):
    text = (destination_items[index]).text
    print("-------")
    print(text)

if len(destination_items) == 1:
    destination_index = '1'
else:
    destination_index = input("Which of the options is your correct destination airport code?\n"
                              "Enter 1 for first, 2 for second, etc. ")

time.sleep(5)
destination_element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "/html/body/ul[2]/li[" + destination_index + "]")))
destination_element.click()  # test passed 12/23/20
time.sleep(6)

# Compute emissions results

compute_button = driver.find_element_by_id("computeByInput")
compute_button.click()  # test passed 12/23/20

# Extract information from the computed ICAO table

table_xpath = "/html/body/div[1]/form/div[2]/div/div/div[1]/div[1]/table/tbody/tr"
time.sleep(15)
table = driver.find_elements_by_xpath(table_xpath)

for row in table:
    print(row)
    tds = row.find_elements_by_tag_name("th")
    table_results = [td.text for td in tds]
    print([td.text for td in tds])
    print(table_results)

# Save computation to a CSV file
# TODO: add flight number to table headers

table_headers = ['Departure Airport', 'Arrival Airport', 'Number of Passengers', 'Cabin Class', 'Trip',
                 'Aircraft Fuel Burn/Journey (KG^ab)', 'Passenger CO2/Journey (KG^c)']
travel_emissions_df = pd.DataFrame(columns=table_headers)
travel_emissions_df.loc[len(travel_emissions_df)] = table_results
travel_emissions_df