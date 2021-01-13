# Import libraries, functions, and PyScraper class

from code.PyScraper import PyScraper
from code import functions_new
import pandas as pd
import time

link = 'https://applications.icao.int/icec'

# Data paths - edit as needed according to system
subset_path         = 'data/concur_flights_working_data_subset.csv'
full_path           = 'data/concur_flights_raw_data.csv'
flight_types_path   = 'data/flight_types.csv'
uniques_path_subset = 'data/uniques_subset.csv'
uniques_path_full   = 'data/uniques_full.csv'
results_path_subset = 'data/output6_subset'
results_path_full   = 'data/output6_full.csv'

# XPATHs for site
one_way_xpath     = '/html/body/div[1]/form/div[1]/div[1]/div/table/tbody/tr/td[1]/select'
cabin_class_xpath = '/html/body/div[1]/form/div[1]/div[1]/div/table/tbody/tr/td[2]/select'
dep_code_xpath    = '/html/body/ul[1]'
arr_code_xpath    = '/html/body/ul[2]'
table_xpath       = '/html/body/div[1]/form/div[2]/div/div/div[1]/div[1]/table/tbody/tr'

start_time = time.time()  # Track the run time of the whole process

subset = pd.read_csv(subset_path)
functions_new.extract_uniques(subset, flight_types_path, uniques_path_subset)  # Extract the unique trips
subset_scrape = PyScraper(link, uniques_path_subset)  # Initialize to scrape just the emissions for the unique trips

# Convert the ticket class types in the data into the correct ICAO categories
subset_tics      = subset_scrape.extract_column('Class of Service')
subset_tics_icao = functions_new.convert_tickets(subset, subset_tics, flight_types_path)

# Extract the airport codes and cities needed to send to ICAO to calculate the emissions
subset_dep_codes  = subset_scrape.extract_column('Departure Station Code')
subset_arr_codes  = subset_scrape.extract_column('Arrival Station Code')
subset_dep_loc    = subset_scrape.extract_column('Departure City')  # this column contains city, state, and country
subset_arr_loc    = subset_scrape.extract_column('Arrival City')
subset_dep_cities = subset_scrape.parse_cities(subset_dep_loc)      # so just the cities are parsed from there
subset_arr_cities = subset_scrape.parse_cities(subset_arr_loc)

next_calc = functions_new.index_of_next_calc(uniques_path_subset)  # get the index of the next row to scrape

if next_calc == -1:  # The 'Emissions (KG)' column is empty, ie nothing has been calculated yet
    print('Starting calculations from first row. Please wait.')

    for index in range(len(subset_dep_codes)):  # For each trip, repeat the following:
        print('Computing: ' + str(index) + ' / ' + str(len(subset_dep_codes)) + '...')

        # Set the appropriate trip settings (ie one way, ticket class) and send the airport and city names to ICAO
        subset_scrape.set_trip_type(one_way_xpath, 'One Way')
        subset_scrape.set_cabin_class(cabin_class_xpath, subset_tics_icao[index])
        subset_scrape.send('frm1', subset_dep_codes[index], subset_dep_cities[index], dep_code_xpath, 'li')
        subset_scrape.send('to1', subset_arr_codes[index], subset_arr_cities[index], arr_code_xpath, 'li')

        subset_scrape.compute()  # Compute the emissions

        # Extract the value
        table = subset_scrape.extract_from_table(table_xpath, 'th')
        emit = table[6]

        # Clear the text box inputs for the next iteration
        subset_scrape.clear_inputs('frm1')
        subset_scrape.clear_inputs('to1')

        # Add the value to the appropriate row in the csv file
        subset_scrape.append_to_csv(emit, index, 'Emissions (KG)', uniques_path_subset)

if next_calc != -1 and next_calc != len(subset_dep_codes):  # The 'Emissions (KG)' column is not empty but not finished

    print('Starting calculations from row ' + str(next_calc) + ". Please wait.")

    for index in range(next_calc, len(subset_dep_codes)):  # For each trip, repeat the following:
        print('Computing: ' + str(index + 1) + ' / ' + str(len(subset_dep_codes)) + '...')

        # Set the appropriate trip settings (ie one way, ticket class) and send the airport and city names to ICAO
        subset_scrape.set_trip_type(one_way_xpath, 'One Way')
        subset_scrape.set_cabin_class(cabin_class_xpath, subset_tics_icao[index])
        subset_scrape.send('frm1', subset_dep_codes[index], subset_dep_cities[index], dep_code_xpath, 'li')
        subset_scrape.send('to1', subset_arr_codes[index], subset_arr_cities[index], arr_code_xpath, 'li')

        subset_scrape.compute()  # Compute the emissions

        # Extract the value
        table = subset_scrape.extract_from_table(table_xpath, 'th')
        emit = table[6]

        # Clear the text box inputs for the next iteration
        subset_scrape.clear_inputs('frm1')
        subset_scrape.clear_inputs('to1')

        # Add the value to the appropriate row in the csv file
        subset_scrape.append_to_csv(emit, index, 'Emissions (KG)', uniques_path_subset)

if next_calc == len(subset_dep_codes):  # The 'Emissions (KG)' column is full, ie all calculations finished
    print('Calculations finished.')

# Now use the unique trips emissions values to fill in the duplicates in the subset

print('Filling in the remaining data. Please wait.')
functions_new.fill_from_uniques(uniques_path_subset, subset_path)  # test passed 1/13/21

print("All done. Finished in: " + str(time.time() - start_time) + "s.")
