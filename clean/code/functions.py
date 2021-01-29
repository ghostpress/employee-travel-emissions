import pandas as pd
import time
import math


def drop_empty_ticket(df, results_path):
    """A function to remove rows in which the 'Ticket ID' field is empty.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe from which to drop the empty ticket rows
    results_path : str
        The path to the file in which to put the remaining rows

    :returns None
    """

    print('Removing rows with empty ticket IDs. Please wait.')
    start = time.time()

    df_copy = df.copy()
    drop = []

    for i, row in df_copy.iterrows():
        if math.isnan(df_copy.at[i, 'Ticket ID']):
            drop.append(i)

    df_copy = df_copy.drop(drop)
    df_copy.to_csv(results_path)
    print('Finished in ' + str((time.time() - start) / 60) + ' mins. ' + 'Please find the remaining data in '
          + results_path + '.')


def drop_zero_distance(df, results_path):
    """A function to remove rows in which the 'Distance' field is 0 miles, or the departure and arrival airport codes
    are the same, eg. BOS to BOS. This operation can edit the original file or create a new one depending on what is
    specified as the results_path parameter.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe from which to drop zero distance rows
    results_path : str
        The path to the file in which to put the remaining rows

    :returns None
    """

    print('Removing rows with zero distance or same departure and arrival airport codes. Please wait.')
    start = time.time()

    df_copy = df.copy()
    drop = []

    for i, row in df_copy.iterrows():

        dep = df_copy.at[i, 'Departure Station Code']
        arr = df_copy.at[i, 'Arrival Station Code']

        if df_copy.at[i, 'Distance (miles)'] == '0':
            drop.append(i)
        if dep is arr:
            drop.append(i)

    df_copy = df_copy.drop(drop)
    df_copy.to_csv(results_path, index=False)
    print('Finished in ' + str((time.time() - start) / 60) + ' mins. ' + 'Please find the remaining data in '
          + results_path + '.')


def parse_date(df, results_path):
    """A function to parse the Departure Date column and create two new columns: Departure Month and Departure Year for
    analysis. Entries in the Departure Date column appear as: 'MMM DD, YYYY'

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe from which to parse the departure date
    results_path : str
        The path to the file to which to add the columns

    :returns None
    """

    print('Parsing flight departure date. Please wait.')
    start = time.time()

    df_copy = df.copy()

    # Create empty columns for the departure month and year to fill from the parsed departure date column
    df_copy['Departure Month'] = ''
    df_copy['Departure Year'] = ''

    for i, row in df_copy.iterrows():
        date = df_copy.at[i, 'Departure Date']
        first_space = date.find(' ')  # Get the index of the first space
        second_space = date.find(' ', first_space + 1, len(date))  # Get the index of the second space

        df_copy.at[i, 'Departure Month'] = date[:first_space]
        df_copy.at[i, 'Departure Year'] = date[second_space + 1:]

    df_copy.to_csv(results_path, index=False)
    print('Finished in ' + str((time.time() - start) / 60) + ' mins. Please find the results in ' + results_path + '.')


def delete_columns(df, columns, results_path):
    """A function to delete a given column from the data.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe in which to delete a given column
    columns : list
        The list of columns to delete
    results_path : str
        The path to file in which to put the remaining data

    :returns None
    """

    print('Deleting the following columns from the data. Please wait. \n' + columns)
    start = time.time()

    df_copy = df.copy()
    df_copy.drop(columns, axis=1)
    df_copy.to_csv(results_path, index=False)

    print('Finished in ' + str((time.time() - start) / 60) + ' mins. Please find the remaining data in '
          + results_path + '.')
