# Import libraries

from collections import Counter


def extract_column(df, column_name):
    """A function to extract a column in a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe from which to extract the column
    column_name : str
        The name of the column to extract into a list

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
        The list of departure airport codes
    arr_list : list
        The list of arrival airport codes

    :returns list
    """

    trips = []

    for index in range(len(dep_list)):
        trips.append(str(dep_list[index]) + " to " + str(arr_list[index]))

    return trips


def count_duplicates(trips):
    """A function to count the duplicates in a list of trips.

    Parameters
    __________
    trips : list
        The list of trips to count

    :returns list
    """

    counter = Counter(trips)
    return counter


def sum_emissions_by_trip(df, trips):
    """A function to sum the emissions from each trip to a certain city.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe from which to get the emissions values
    trips : list
        The list of trips of which to sum the emissions

    :returns dictionary
    """

    emissions = {}  # Create an empty dictionary with trip : emissions key : value pairs
    index_of_to = -1

    for i, row in df.iterrows():
        for j in range(len(trips)):

            index_of_to = trips[j].find('to')
            from_city = trips[j][:index_of_to]
            to_city = trips[j][index_of_to:]

            if df.at[i, 'Departure City'] == from_city and df.at[i, 'Arrival City'] == to_city:
                emissions[trips[j]] += df.at[i, 'Emissions (MT CO2)']

    return emissions

