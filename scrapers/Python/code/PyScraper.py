# Import Libraries

from bs4 import BeautifulSoup
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from csv import reader
from csv import writer
# import requests
import time
import pandas as pd
import numpy as np

from code.chromedriver import chrome_driver


class PyScraper:
    # Global attributes / fields: website link, driver object, path to data.csv, and dataframe
    global link
    global driver
    global data_path
    global df

    def __init__(self, url, path):

        # Initiate the driver

        link = url
        self.driver = chrome_driver(link)
        data_path = path

        # Load web elements into BeautifulSoup

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Get dataframe from csv in data_path
        self.df = pd.read_csv(data_path)

    @staticmethod
    def get_driver():  # TODO: delete
        return driver

    @staticmethod
    def get_html(self):  # TODO: delete
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

        for item in entries:  # For each item in the entire list of entries,

            index = item.find(',')  # find the index of the first comma
            cities.append(item[0:index])  # append the substring containing the city name to the list

        return cities

    def set_trip_type(self, xpath, type):
        """A function to set and click the correct trip type in the calculator.

        Parameters
        ----------
        xpath : str
            The XPATH of the trip type drop-down menu
        type : str
            The desired trip type
        """

        select = Select(self.driver.find_element_by_xpath(xpath))
        select.select_by_visible_text(type)
        time.sleep(2)  # Selenium runs very quickly, website can't always load elements in time

    def match(self, airport, city, items):
        # TODO: remove airport field? maybe use both to match
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

        items_str = []
        for item in items:
            items_str.append(item.text)

        correct_index = -1

        if len(items_str) == 1:
            correct_index = 1
        else:
            to_match = self.parse_cities(items_str)  # extract just the cities from each row in the menu

            for i in range(len(to_match)):
                if to_match[i] == city.upper():
                    correct_index = i + 1  # web menu lists start from index 1 for some dumb reason

        return correct_index

    def send(self, name, airport, city, xpath, tag_name):
        """A function to send airport info to the online ICAO calculator.

        Parameters
        ----------
        name : str
            The input to the driver, eg. 'frm1' for departure
        airport : str
            The airport code, eg. BOS
        xpath : str
            The XPATH of the drop-down menu
        tag_name : str
        """

        input = self.driver.find_element_by_name(name)
        input.send_keys(airport)
        time.sleep(2)

        click_wait = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        menu_items = click_wait.find_elements_by_tag_name(tag_name)  # list of drop-down menu options
        # print(type(menu_items))  # list; FIXME: call to match() raises 'WebElement' not iterable error
        # print(type(menu_items[0]))  # WebElement; should be str

        # Click the correct option, using the match() helper function

        index = self.match(airport, city, menu_items)
        element = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, xpath + "/" + tag_name + "[" + str(index) + "]")))
        element.click()

    def compute(self, id):
        """A function to have the ICAO calculator compute the emissions.

        Parameters
        ----------
        id : str
            The id of the WebElement for the compute button
        """

        button = self.driver.find_element_by_id(id)
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

        time.sleep(5)  # Was 15, still works so far 1/8/21

        table = self.driver.find_elements_by_xpath(xpath)

        for row in table:
            tds = row.find_elements_by_tag_name(tag_name)
            table_results = [td.text for td in tds]

        return table_results

    def append_to_csv(self, new_val, row, col):
        """A function to add a value to a csv file in the specified row and column.

        Parameters
        ----------
        new_val : int
            The new value to append in the correct column and row
        row : int
            The row in which to insert the new value

        :returns str
        """

        self.df.at[row, col] = new_val
        self.df.to_csv('output2.csv', index=False)

    def clear_inputs(self, name):
        """A function to clear the inputs on the page, so that the next iteration can be entered.

        Parameters
        ----------
        name : str
            The name of the input to clear.
        """

        input_to_clear = self.driver.find_element_by_name(name)
        input_to_clear.clear()

    def convert_tickets(self, tics, format_file):
        """A function to convert the ticket class names into the matching ICAO categories: Economy or Premium.
        Ticket classes are not standard across airlines, and there are many different names for the same class.

        Parameters
        ----------
        tics : list
            The list of ticket classes taken from the dataset.
        format_file : str
            The path to the file which contains the conversions to ICAO categories.

        :returns list
        """

        convert_guide = pd.read_csv(format_file)  # makes the file into a dataframe for easy access
        self.df['ICAO Trip Category'] = ''

        for index in range(len(tics)):
            for i, row in convert_guide.iterrows():
                # print(convert_guide.at[i, "Field in Sheet"])
                if tics[index] == convert_guide.at[i, "Field in Sheet"]:

                    self.df.at[index, 'ICAO Trip Category'] = convert_guide.at[i, "Change to"]

        return self.df['ICAO Trip Category'].tolist()

    # def extract_column_uniques(self):  # TODO: write for later
