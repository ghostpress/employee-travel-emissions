# Import libraries
import pandas as pd
import numpy as np

# Read csv file into DataFrame
df_subset = pd.read_csv('concur_flights_working_data_subset.csv')
# print(df_subset.to_string())
test = df_subset.get('Departure Station Code')
# print(test)
# print(type(test))
# print(test.get(2))

# Extract departure and arrival codes for each trip into a dictionary to count them
# Key is [departure, arrival] and value is count

# First, get the codes in a list
trips_list = np.empty([42, 2], dtype=str)  # initialize empty string list w/ 42 rows, 2 columns

for index, row in df_subset.iterrows():
    trips_list[(row, 0)] = row[7]   # departure station codes in column 7
    trips_list[(row, 1)] = row[13]  # arrival station codes in column 13
    print(trips_list)

# for row in range(0, 42):
    # trips_list[row][0] = (df_subset.get('Departure Station Code')).get(row)
    # trips_list[row][1] = (df_subset.get('Arrival Station Code')).get(row)

print(trips_list)

# Now count the instances of each departure-arrival pair

