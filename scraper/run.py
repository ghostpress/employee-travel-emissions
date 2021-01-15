# Import libraries, functions, and PyScraper class

from code.PyScraper import PyScraper
from code import functions
import pandas as pd
import time

link = 'https://applications.icao.int/icec'

# Data paths - edit as needed according to system
subset_path         = 'data/concur_flights_working_data_subset.csv'
full_path           = 'data/concur_flights_raw_data.csv'
flight_types_path   = 'data/flight_types.csv'
uniques_path_subset = 'data/uniques_subset.csv'
uniques_path_full   = 'data/uniques_full.csv'

# XPATHs for site
one_way_xpath     = '/html/body/div[1]/form/div[1]/div[1]/div/table/tbody/tr/td[1]/select'
cabin_class_xpath = '/html/body/div[1]/form/div[1]/div[1]/div/table/tbody/tr/td[2]/select'
dep_code_xpath    = '/html/body/ul[1]'
arr_code_xpath    = '/html/body/ul[2]'
table_xpath       = '/html/body/div[1]/form/div[2]/div/div/div[1]/div[1]/table/tbody/tr'

start_time = time.time()  # Track the run time of the whole process

full_data = pd.read_csv(full_path)
functions.extract_uniques(full_data, flight_types_path, uniques_path_full)  # Extract the unique trips
full_scrape = PyScraper(link, uniques_path_full)  # Initialize to scrape just the emissions for the unique trips

# Convert the ticket class types in the data into the correct ICAO categories
subset_tics      = full_scrape.extract_column('Class of Service')
subset_tics_icao = functions.convert_tickets(full_data, subset_tics, flight_types_path)

# Extract the airport codes and cities needed to send to ICAO to calculate the emissions
full_dep_codes  = full_scrape.extract_column('Departure Station Code')
full_arr_codes  = full_scrape.extract_column('Arrival Station Code')
full_dep_loc    = full_scrape.extract_column('Departure City')  # this column contains city, state, and country
full_arr_loc    = full_scrape.extract_column('Arrival City')
full_dep_cities = full_scrape.parse_cities(full_dep_loc)        # so just the cities are parsed from there
full_arr_cities = full_scrape.parse_cities(full_arr_loc)

# Have to skip some rows b/c code pairing doesn't work in calculator - must not have been a direct flight
skip_list = [27, 33, 245, 261, 400, 500, 511, 513, 526, 527, 546, 565, 583, 600, 611, 620, 660, 687, 714, 738, \
                 852, 883, 884, 887, 909, 937, 950, 1041, 1048, 1096]
next_calc = functions.index_of_next_calc(uniques_path_full, skip_list)  # get the index of the next row to scrape

if next_calc == -1:  # The 'Emissions (KG)' column is empty, ie nothing has been calculated yet
    print('Starting calculations from first row. Please wait.')

    for index in range(len(full_dep_codes)):  # For each trip, repeat the following:
        print('Computing: ' + str(index + 1) + ' / ' + str(len(full_dep_codes)) + '...')
        print('Time: ' + str((time.time() - start_time)/60) + " mins.")

        # Set the appropriate trip settings (ie one way, ticket class) and send the airport and city names to ICAO
        full_scrape.set_trip_type(one_way_xpath, 'One Way')
        full_scrape.set_cabin_class(cabin_class_xpath, subset_tics_icao[index])
        full_scrape.send('frm1', full_dep_codes[index], full_dep_cities[index], dep_code_xpath, 'li')
        full_scrape.send('to1', full_arr_codes[index], full_arr_cities[index], arr_code_xpath, 'li')

        full_scrape.compute()  # Compute the emissions

        # Extract the value
        table = full_scrape.extract_from_table(table_xpath, 'th')
        emit = table[6]

        # Clear the text box inputs for the next iteration
        full_scrape.clear_inputs('frm1')
        full_scrape.clear_inputs('to1')

        # Add the value to the appropriate row in the csv file
        full_scrape.append_to_csv(emit, index, 'Emissions (KG)', uniques_path_full)

if next_calc != -1 and next_calc != len(full_dep_codes):  # The 'Emissions (KG)' column is not empty but not finished

    if next_calc in skip_list:
        next_calc += 1
        print('Skipping ' + str(next_calc) + " for now.")

    print('Starting calculations from row ' + str(next_calc) + ". Please wait.")

    for index in range(next_calc, len(full_dep_codes)):  # For each trip, repeat the following:
        print('Computing: ' + str(index + 1) + ' / ' + str(len(full_dep_codes)) + '...')
        print('Time: ' + str((time.time() - start_time)/60) + " mins.")

        # Set the appropriate trip settings (ie one way, ticket class) and send the airport and city names to ICAO
        full_scrape.set_trip_type(one_way_xpath, 'One Way')
        full_scrape.set_cabin_class(cabin_class_xpath, subset_tics_icao[index])
        full_scrape.send('frm1', full_dep_codes[index], full_dep_cities[index], dep_code_xpath, 'li')
        full_scrape.send('to1', full_arr_codes[index], full_arr_cities[index], arr_code_xpath, 'li')

        full_scrape.compute()  # Compute the emissions

        # Extract the value
        table = full_scrape.extract_from_table(table_xpath, 'th')
        emit = table[6]

        # Clear the text box inputs for the next iteration
        full_scrape.clear_inputs('frm1')
        full_scrape.clear_inputs('to1')

        # Add the value to the appropriate row in the csv file
        full_scrape.append_to_csv(emit, index, 'Emissions (KG)', uniques_path_full)

if next_calc == len(full_dep_codes):  # The 'Emissions (KG)' column is full, ie all calculations finished
    print('Calculations finished.')

# Now use the unique trips emissions values to fill in the duplicates in the subset

print('Filling in the remaining data. Please wait.')
functions.fill_from_uniques(uniques_path_full, full_path)  # test passed 1/13/21

print("All done. Finished in: " + str((time.time() - start_time)/60) + " mins.")
