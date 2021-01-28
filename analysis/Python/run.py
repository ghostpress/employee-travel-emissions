# Import libraries and functions

import pandas as pd
from code import functions
import plotly.graph_objects as go

# Read csv file into DataFrame
df_subset = pd.read_csv('data/concur_flights_working_data_subset.csv')  # subset to test
df_full = pd.read_csv('data/cleaned_full.csv')                          # full data set, incl. emissions

# Using the functions, get the departure and arrival cities

dep_list = functions.extract_column(df_full, 'Departure City')
arr_list = functions.extract_column(df_full, 'Arrival City')

trips = functions.combine_codes(dep_list, arr_list)  # Combine the two lists into one

# Now count the number of trips
dups = functions.count_duplicates(trips)

most_common = dups.most_common(5)  # Get the 5 most common routes
freq = dups.values()               # Get the list of counts

# Make a table
table = go.Figure(data=[go.Table(
    header=dict(values=['Rank', 'Route', 'Number of Trips'],
                line_color='black',
                fill_color='white',
                align='left'),
    cells=dict(values=[[1, 2, 3, 4, 5],        # First column
                       most_common,            # Second column
                       list(dups.values())],   # Third column
               line_color='black',
               fill_color='white',
               align='left'))
])

print('Table correctly created.')
