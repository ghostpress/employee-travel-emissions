# Import libraries and classes

import pandas as pd
import math
from code import PyScraper


def convert_tickets(df, tickets, format_file):
    """A function to convert the ticket class names into the matching ICAO categories: Economy or Premium.
    Ticket classes are not standard across airlines, and there are many different names for the same class.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe holding the original dataset, including ticket types to convert
    tickets : list
        The list of ticket classes taken from the dataset
    format_file : str
        The path to the file which contains the conversions to ICAO categories

    :returns list
    """

    convert_guide = pd.read_csv(format_file)
    df['ICAO Trip Category'] = ''  # Create a new column for the converted ticket types

    for index in range(len(tickets)):
        for i, row in convert_guide.iterrows():
            if tickets[index] == convert_guide.at[i, "Field in Sheet"]:
                df.at[index, 'ICAO Trip Category'] = convert_guide.at[i, "Change to"]

    return df['ICAO Trip Category'].tolist()


def extract_uniques(df_orig):
    """A function to extract the unique trips according to departure and arrival airport codes, and cabin class.
    The output is printed to a new csv file.

    Parameters
    ----------
    df_orig : pd.DataFrame
        The dataframe holding the original data from which to extract unique trips

    :returns str
    """

    print('Extracting unique trips. Please wait.')

    df_copy = df_orig.copy()  # Make a copy of the dataframe currently holding all data

    # Create a new column combining the trip info: 'DEP ARR Class' (blank for now)
    df_copy['Trip Info Combined'] = ''

    # Call helper function convert_tickets()
    tickets = convert_tickets(df_copy, df_copy['Class of Service'].values.tolist(), 'data/flight_types.csv')

    # Fill in that column
    df_copy['Trip Info Combined'] = df_copy['Departure Station Code'] + " " + df_copy['Arrival Station Code'] + " " + \
                                    df_copy['ICAO Trip Category']

    df_uniques = df_copy.drop_duplicates(subset='Trip Info Combined')  # Drop the duplicates
    df_uniques.to_csv('data/unique_trips_full.csv', index=False)       # Write to a csv file in the data folder
    return 'data/unique_trips_full.csv'


def index_of_next_calc(results_path):
    """A function to get the index of the next row to calculate in the emissions output file.
     Use in case the browser crashes, keyboard interrupt, Selenium error stops the program, etc. to continue scraping
     without repeating previous work.

    Parameters
    ----------
    results_path : str
        The path to the file to which the scraper had been writing

    :returns int
    """

    last_place = -2  # Initialize as -2 to test if all values calculated
    df_results = pd.read_csv(results_path)

    for i, row in df_results.iterrows():
        if math.isnan(df_results.at[i, 'Emissions']):  # Check if empty entry, ie not yet calculated
            last_place = i
            break  # Exit the loop; otherwise, it will keep going until the end of the file

    return last_place + 1  # if -1 is returned, then all values have been calculated


def fill_from_uniques(uniques_path, all_path):  # TODO: test
    """A function to backfill duplicate emissions calculations from a file containing the unique trips and their emissions.

    Parameters
    ----------
    uniques_path : str
        The path to the file containing the unique trips and emissions calculations
    all_path : str
        The path to the file containing all the data to be back-filled

    :returns None
    """

    # Create dataframes from the csv files for easy iteration
    uniques = pd.read_csv(uniques_path)
    all_data = pd.read_csv(all_path)

    data_copy = all_data.copy()  # Create a copy of the data
    convert_tickets(data_copy, data_copy['Class of Service'].values.tolist(), 'data/flight_types.csv')
    data_copy['Trip Info Combined'] = data_copy['Departure Station Code'] + " " + data_copy['Arrival Station Code'] + \
                                      " " + data_copy['ICAO Trip Category']

    data_copy['Emissions'] = ''  # Create an empty column in the data file for the emissions calculations

    for i, row in data_copy.iterrows():
        for j, row_ in uniques.iterrows():
            if data_copy.at[i, 'Trip Info Combined'] == uniques.at[j, 'Trip Info Combined']:  # if the trip info matches
                data_copy.at[i, 'Emissions'] = uniques.at[j, 'Emissions']                     # copy the value in

    data_copy.to_csv('data/filled.csv')

    print('Duplicate trips back-filled.')


# TODO: write a helper method for combining the trip info; pass in the file names to these ^ methods, ie subset vs all, etc.
# TODO: change 'Emissions' column to 'Emissions (KG)'