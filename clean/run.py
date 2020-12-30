# Import libraries
import pandas as pd

# Read csv file into DataFrame
df_subset = pd.read_csv('concur_flights_working_data_subset.csv')

# Remove duplicates
df_subset_unique = df_subset.drop_duplicates()

# Write to new csv file
compression_opts = dict(method='zip', archive_name='subset_unique.zip')
df_subset_unique.to_csv('subset_unique.zip', index=False, compression=compression_opts)
print("Duplicates removed.")
