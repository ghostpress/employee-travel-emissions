# Import Libraries

from bs4 import BeautifulSoup
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# import requests
# import time
import pandas as pd
import numpy as np

from code.chromedriver import chrome_driver


class PyScraper:
    global link
    global driver
    global data_path
    global df

    def __init__(self, url, path):
        # Initiate the driver

        link = url
        driver = chrome_driver(link)
        data_path = path

        # Load web elements into BeautifulSoup

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Get dataframe from csv in data_path
        self.df = pd.read_csv(data_path)

    @staticmethod
    def test_class(self):  # TODO: before final production version, delete this
        return 0

    @staticmethod
    def get_driver():
        return driver

    @staticmethod
    def get_html(self):
        return driver.page_source

    def extract_column(self, col_name):
        """A function to extract the items in a specified column in the data.

        Parameters
        ----------
        col_name : str
            The name of the column from which to extract the items.

        :returns list
        """

        list = self.df[col_name].values.tolist()
        return list

    def parse_cities(self, entries):
        """A function to parse the city name from the longer entry in the corresponding column.
        For example, Boston is listed as 'Boston, MASSACHUSETTS, US', so this function returns just
        'Boston'.

        Parameters
        ----------
        entries : list
            The list of entries from which to extract only each city name

        :returns list
        """

        # Entries always in the following format: CityName, STATENAME, COUNTRYABBREV
        cities = []

        for item in entries:              # For each item in the entire list of entries,

            index = item.find(',')        # find the index of the first comma
            cities.append(item[0:index])  # append the substring containing the city name to the list

        return cities

    def match(self, airport, city, items):
        """A function to match the given airport code to the correct option in the drop-down menu.

        Parameters
        ----------
        airport : str
            The airport code, eg. BOS
        city : str
            The full name of the city, eg. Boston
        items : list
            The options in the drop-down menu; index starts from 1

        :returns int
        """

        if len(items) == 1:
            correct_index = 1
        else:
            city.upper()
            for i in range(len(items)):
                if city in items[i]:
                    correct_index = i

        return correct_index

    def send(self, input, airport, city, xpath, tag_name):
        """A function to send airport info to the online ICAO calculator.

        Parameters
        ----------
        input : WebElement
            The input to the driver, eg. 'frm1' for departure
        airport : str
            The airport code, eg. BOS
        xpath : str
            The XPATH of the drop-down menu
        tag_name : str
        """

        input.send_keys(airport)
        click_wait = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        menu_items = click_wait.find_elements_by_tag_name(tag_name)  # list of drop-down menu options

        # Click the correct option, using the match() helper function

        index = match(airport, city, menu_items)
        element = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, xpath + "/" + tag_name + "[" + index + "]")))
        element.click()

    def compute_click(self, id):
        """A function to have the ICAO calculator compute the emissions.

        Parameters
        ----------
        id : str
            The id of the WebElement for the compute button
        """

        button = driver.find_element_by_id(id)
        button.click()

    def extract_from_table(self, xpath, tag_name):
        """A function to extract the emissions figures from the ICAO calculator table.

        Parameters
        ----------
        xpath : str
            The XPATH of the table
        tag_name : str

        :returns list
        """

        table = driver.find_elements_by_xpath(xpath)

        for row in table:
            tds = row.find_elements_by_tag_name(tag_name)
            table_results = [td.text for td in tds]

        return table_results

    def append_to_csv(self, csv, emissions_list):
        """A function to add the computed emissions to the rows of an existing data.csv file.
        """

        data = pd.read_csv(csv)

        trips = airports_from_csv(data)  # Get the airport codes using helper function
        # TODO: finish this

    def airports_from_csv(self, csv):
        """A function to read the rows of a data.csv file and extract the airport codes for computing emissions.

        Parameters
        ----------
        csv : str
            file path of the data.csv file from which to extract airport departure & arrival codes

        :returns list
        """

        data = pd.read_csv(csv)  # Create dataframe from data.csv

        dep_list = data['Departure Station Code'].values.tolist()  # Extract departure codes column into a list
        arr_list = data['Arrival Station Code'].values.tolist()  # Extract arrival codes column into a list

        trips_list = np.array((dep_list, arr_list))  # Combine the two lists into one
        trips_list = trips_list.T  # Transpose the list to get [[dep, arr]]

        return trips_list

    def cities_from_csv(self, csv):
        """A function to read the rows of a data.csv file and extract the cities for computing emissions.

        Parameters
        ----------
        csv : str
            file path of the data.csv file from which to extract airport departure & arrival codes

        :returns list
        """

        data = pd.read_csv(csv)  # Create dataframe from data.csv

        dep_city_list = data['Departure City']  # Extract departure cities column into a list
        arr_city_list = data['Arrival City']  # Extract arrival cities column into a list

        cities_list = np.array((dep_city_list, arr_city_list))  # Combine the two lists into one
        cities_list = cities_list.T  # Transpose the list to get [[dep, arr]]

        return cities_list
