import pandas as pd
from code import functions

# Data paths - edit according to system
data_path_subset = 'data/concur_flights_working_data_subset.csv'  # subset to test
data_path_full = 'data/flights.csv'                               # full data

# Create a dataframe from the desired data file
data_df = pd.read_csv(data_path_full)

# Drop any rows in the data with 0 distance or in which the departure and arrival airport codes are the same
functions.drop_zero_distance(data_df, data_path_full)

# Drop any rows in the data with empty ticket IDs
functions.drop_empty_ticket(data_df, data_path_full)

# Create new columns for the departure month and year, using the departure date column
functions.parse_date(data_df, data_path_full)
