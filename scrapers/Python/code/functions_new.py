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
    df_copy['Trip Info Combined'] = df_copy['Departure Station Code'] + " " + df_copy['Arrival Station Code'] + " " + df_copy['ICAO Trip Category']
    df_uniques = df_copy.drop_duplicates(subset='Trip Info Combined')  # drop the duplicates

    return df_uniques.to_csv('unique_trips.csv', index=False)  # FIXME: returns 'None' & also the csv file is in the working directory, not /data/


# def backfill_from_uniques():
