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
dups = count_duplicates(trips)

most_common = dups.most_common(5)  # Get the 5 most common routes
# print(most_common)

freq = dups.values()
print(list(freq))

# Make a table
table = go.Figure(data=[go.Table(
    header=dict(values=['Rank', 'Route', 'Number of Trips'],
                line_color='black',
                fill_color='white',
                align='left'),
    cells=dict(values=[[1, 2, 3, 4, 5],  # First column
                       most_common,      # Second column
                       list(dups.values())],   # Third column
               line_color='black',
               fill_color='white',
               align='left'))
])

print('Table correctly created.')
table.update_layout(width=500, height=300)
table.show

