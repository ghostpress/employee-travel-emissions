# Import libraries and functions

import pandas as pd
from functions import *
import plotly.graph_objects as go

# Read csv file into DataFrame
df_subset = pd.read_csv('concur_flights_working_data_subset.csv')  # subset to test

# ------- Functions for counting and displaying in a table the most frequent routes in the data -------

# Using the functions, get the codes into a single list

dep_list = airport_codes_from_df(df_subset, 'Departure Station Code')
arr_list = airport_codes_from_df(df_subset, 'Arrival Station Code')

trips = combine_codes(dep_list, arr_list)

# Now count the duplicate trips
print(count_duplicates(trips))  # print test passed 1/7/21

# Make a table


