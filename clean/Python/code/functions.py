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
    df_copy.to_csv(results_path)
    print('Finished in ' + str((time.time() - start) / 60) + ' mins. ' + 'Please find the remaining data in '
          + results_path + '.')
