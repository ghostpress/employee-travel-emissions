# Import libraries

from collections import Counter


def airport_codes_from_df(df, column_name):
    """A function to extract a list of airport codes from the correct column in a dataframe.

    Parameters
    ----------
    df : DataFrame
        the dataframe from which to extract the codes
    column_name : str
        the name of the column to extract into a list

    :returns list
    """

    list = df[column_name].values.tolist()

    return list


def combine_codes(dep_list, arr_list):
    """A function to combine the lists of departure and arrival airport codes into one list,
    where each element is of the form DEP ARR

    Parameters
    __________
    dep_list : list
        the list of departure airport codes
    arr_list : list
        the list of arrival airport codes

    :returns list
    """

    trips = []

    for index in range(len(dep_list)):
        trips.append(dep_list[index] + " " + arr_list[index])

    return trips

def count_duplicates(trips):
    """A function to count the duplicates in a list of trips.

    Parameters
    __________
    trips : list
        the list of trips, where each element is in the form DEP ARR

    :returns list
    """

    counter = Counter(trips)
    return counter
