# Import libraries
import pandas as pd
import numpy as np

# Read csv file into DataFrame
df_subset = pd.read_csv('concur_flights_working_data_subset.csv')

# Extract departure and arrival codes for each trip into a dictionary to count them
# Key is [departure, arrival] and value is count

# First, get the codes in a list

dep_list = df_subset['Departure Station Code'].values.tolist()  # extract departure code column into list
arr_list = df_subset['Arrival Station Code'].values.tolist()    # extract arrival code column into list

trips_list = np.array((dep_list, arr_list))  # combine the two lists into one
trips_list = trips_list.T  # transpose the list to get [[arr, dep]]
print(trips_list)  # print test passed 1/6/21

# Now count the instances of each departure-arrival pair

count = np.zeros(42, dtype=int)  # initialize array for counting trips
print(count)  # print test passed 1/6/21


