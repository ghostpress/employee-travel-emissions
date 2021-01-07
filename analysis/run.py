# Import libraries and functions

import pandas as pd
import analysis.functions

# Read csv file into DataFrame
df_subset = pd.read_csv('concur_flights_working_data_subset.csv')

# Using the functions, get the codes into a single list

dep_list = analysis.airport_codes_from_df('Departure Station Code')
arr_list = analysis.airport_codes_from_df('Arrival Station Code')

trips = analysis.combine_codes(dep_list, arr_list)

# Now count the duplicate trips
print(analysis.count_duplicates(trips))


