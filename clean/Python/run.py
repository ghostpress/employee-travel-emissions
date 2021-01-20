import pandas as pd
from code import functions

data_path = 'data/concur_flights_working_data_subset.csv'  # subset to test
data_df = pd.read_csv(data_path)

# Drop any rows in the data with 0 distance or in which the departure and arrival airport codes are the same
functions.drop_zero_distance(data_df, data_path)