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


def extract_uniques(df_orig):  # TODO: make it return a df
    """A function to extract the unique trips according to departure and arrival airport codes, and cabin class.

    Parameters
    ----------
    df_orig : pd.DataFrame
        The dataframe holding the original data from which to extract unique trips

    :returns list
    """

    df_copy = df_orig.copy()  # Make a copy of the dataframe currently holding all data

    # Create a new column combining the trip info: 'DEP ARR Class'

    df_copy['Trip Info Combined'] = ''

    # Call convert_tickets() first TODO: make this cleaner
    tickets = convert_tickets(df_copy, df_copy['Class of Service'].values.tolist(), 'data/flight_types.csv')

    df_copy['Trip Info Combined'] = df_copy['Departure Station Code'] + " " + df_copy['Arrival Station Code'] + " " + df_copy['ICAO Trip Category']

    combined_list = df_copy['Trip Info Combined'].values.tolist()
    uniques = []

    for item in combined_list:
        if item not in uniques:
            uniques.append(item)

    return uniques