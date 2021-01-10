# Import libraries and classes

import pandas as pd
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

    df_copy = df_orig.copy()  # Make a copy of the dataframe currently holding all data

    # Create a new column combining the trip info: 'DEP ARR Class' (blank for now)
    df_copy['Trip Info Combined'] = ''

    # Call helper function convert_tickets()
    tickets = convert_tickets(df_copy, df_copy['Class of Service'].values.tolist(), 'data/flight_types.csv')

    # Fill in that column
    df_copy['Trip Info Combined'] = df_copy['Departure Station Code'] + " " + df_copy['Arrival Station Code'] + " " + \
                                    df_copy['ICAO Trip Category']

    df_uniques = df_copy.drop_duplicates(subset='Trip Info Combined')  # Drop the duplicates
    df_uniques.to_csv('data/unique_trips.csv', index=False)  # Write to a csv file in the data folder
    return 'data/unique_trips.csv'


def fill_from_uniques(uniques_path, all_path):
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

    data_copy['Emissions'] = ''  # Create an empty column in the data file for the emissions calculations

    for i, row in data_copy.iterrows():
        for j, row_ in uniques.iterrows():
            if data_copy.at[i, 'Trip Info Combined'] == uniques.at[j, 'Trip Info Combined']:  # if the trip info matches
                data_copy.at[i, 'Emissions'] = uniques.at[j, 'Emissions']                     # copy the value in

    data_copy.to_csv('data/filled.csv')

    print('Duplicate trips back-filled.')
