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

# --------------------- TESTING BELOW THIS LINE ---------------------

print('Testing.')

subset = pd.read_csv(subset_path)
# functions_new.extract_uniques(subset, flight_types_path, uniques_path_subset)  # commented out to test next_calc
subset_scrape = PyScraper(link, uniques_path_subset)  # for now, scrape just the unique values and fill back later TODO: set to results file

subset_tics      = subset_scrape.extract_column('Class of Service')
subset_tics_icao = functions_new.convert_tickets(subset, subset_tics, flight_types_path)

subset_dep_codes  = subset_scrape.extract_column('Departure Station Code')
subset_arr_codes  = subset_scrape.extract_column('Arrival Station Code')
subset_dep_loc    = subset_scrape.extract_column('Departure City')
subset_arr_loc    = subset_scrape.extract_column('Arrival City')
subset_dep_cities = subset_scrape.parse_cities(subset_dep_loc)
subset_arr_cities = subset_scrape.parse_cities(subset_arr_loc)

next_calc = functions_new.index_of_next_calc(uniques_path_subset)  # TODO NEXT!!
print(str(next_calc))  # FIXME: says 4 when should be 11

quit()

if next_calc == -1:

    print('Starting calculations from first row. Please wait.')
    for index in range(len(subset_dep_codes)):

        print('Computing: ' + str(index + 1) + ' / ' + str(len(subset_dep_codes)) + '...')

        subset_scrape.set_trip_type(one_way_xpath, 'One Way')
        subset_scrape.set_cabin_class(cabin_class_xpath, subset_tics_icao[index])
        subset_scrape.send('frm1', subset_dep_codes[index], subset_dep_cities[index], dep_code_xpath, 'li')
        subset_scrape.send('to1', subset_arr_codes[index], subset_arr_cities[index], arr_code_xpath, 'li')

        subset_scrape.compute()

        table = subset_scrape.extract_from_table(table_xpath, 'th')
        emit = table[6]

        subset_scrape.clear_inputs('frm1')
        subset_scrape.clear_inputs('to1')

        subset_scrape.append_to_csv(emit, index, 'Emissions (KG)', uniques_path_subset)  # edit uniques file for now

if next_calc != -1:  # FIXME: on 2nd keyboard interrupt (at row 10 completed), still says row 5

    print('Starting calculations from row ' + str(next_calc) + ". Please wait.")
    for index in range(next_calc, len(subset_dep_codes)):
        print('Computing: ' + str(index + 1) + ' / ' + str(len(subset_dep_codes)) + '...')

        subset_scrape.set_trip_type(one_way_xpath, 'One Way')
        subset_scrape.set_cabin_class(cabin_class_xpath, subset_tics_icao[index])
        subset_scrape.send('frm1', subset_dep_codes[index], subset_dep_cities[index], dep_code_xpath, 'li')
        subset_scrape.send('to1', subset_arr_codes[index], subset_arr_cities[index], arr_code_xpath, 'li')

        subset_scrape.compute()

        table = subset_scrape.extract_from_table(table_xpath, 'th')
        emit = table[6]

        subset_scrape.clear_inputs('frm1')
        subset_scrape.clear_inputs('to1')

        subset_scrape.append_to_csv(emit, index, 'Emissions (KG)', uniques_path_subset)

# print(next_calc)  # print test passed 1/12/21

# print(pd.read_csv('output6_full.csv')['Emissions'])

# functions_new.extract_uniques(pd.read_csv(full_path), flight_types_path, results_path)  # Run once to extract uniques
# test_scrape = PyScraper(link, results_path)
#
# test_tic_list = test_scrape.extract_column('Class of Service')
# test_tic_list_icao = functions_new.convert_tickets(test_scrape.get_df(), test_tic_list, flight_types_path)
# test_dep_codes = test_scrape.extract_column('Departure Station Code')
# test_arr_codes = test_scrape.extract_column('Arrival Station Code')
# test_dep_loc = test_scrape.extract_column('Departure City')
# test_arr_loc = test_scrape.extract_column('Arrival City')
# test_dep_city = test_scrape.parse_cities(test_dep_loc)
# test_arr_city = test_scrape.parse_cities(test_arr_loc)
# test_emissions = []

# next_calc = functions_new.index_of_next_calc(results_path)
#
# if next_calc != -1:
#
#     print('Computing where last left off. Please wait.')
#     for index in range(next_calc, len(test_dep_codes)):
#
#         print("Computing: " + str(index + 1) + " / " + str(len(test_dep_codes)) + " ...")
#         test_scrape.compute()
#         table = test_scrape.extract_from_table("/html/body/div[1]/form/div[2]/div/div/div[1]/div[1]/table/tbody/tr",
#                                                  "th")
#         test_emissions.append(table[6])
#
#         test_scrape.clear_inputs('frm1')
#         test_scrape.clear_inputs('to1')
#
#         test_csv = test_scrape.append_to_csv(test_emissions[index], index, 'Emissions')
#
# if next_calc == -1:
#
#     print('Computing. Please wait.')
#
#     for index in range(len(test_dep_codes)):
#
#         print("Computing: " + str(index + 1) + " / " + str(len(test_dep_codes)) + " ...")
#         test_scrape.compute()
#         table = test_scrape.extract_from_table("/html/body/div[1]/form/div[2]/div/div/div[1]/div[1]/table/tbody/tr",
#                                                  "th")
#         test_emissions.append(table[6])
#
#         test_scrape.clear_inputs('frm1')
#         test_scrape.clear_inputs('to1')
#
#         test_csv = test_scrape.append_to_csv(test_emissions[index], index, 'Emissions')

# print(functions_new.index_of_next_calc('output6_full.csv'))  # first print test passed 1/11/21
print('No longer testing.')
quit()

# ------------------- DEVELOPMENT BELOW THIS LINE --------------------

# Run once to extract unique data into file - this will take a while for the full set
# uniques_path = functions_new.extract_uniques(pd.read_csv(full_path))

# Initialize the scraper
unique_scrape = PyScraper(link, 'data/unique_trips_full.csv')

# Get the list of ticket classes
unique_tic_list = unique_scrape.extract_column('Class of Service')

# Put the ticket class list into the correct categories for ICAO  FIXME: doesn't change original file
unique_tic_list_icao = functions_new.convert_tickets(unique_scrape.get_df(), unique_tic_list, flight_types_path)

# Get the departure and arrival airport codes
unique_dep_list = unique_scrape.extract_column('Departure Station Code')
unique_arr_list = unique_scrape.extract_column('Arrival Station Code')

# Get the entries in the departure and arrival cities
unique_dep_loc = unique_scrape.extract_column('Departure City')
unique_arr_loc = unique_scrape.extract_column('Arrival City')

# Parse the city names from these
unique_dep_city = unique_scrape.parse_cities(unique_dep_loc)
unique_arr_city = unique_scrape.parse_cities(unique_arr_loc)

unique_emissions = []
start_time = time.time()  # Want to get running time for computation
print('Computing. Please wait.')

for index in range(len(unique_dep_list)):

    # Set the trip type (all one way)
    unique_scrape.set_trip_type('/html/body/div[1]/form/div[1]/div[1]/div/table/tbody/tr/td[1]/select', 'One Way')

    # Set the cabin class category
    unique_scrape.set_cabin_class('/html/body/div[1]/form/div[1]/div[1]/div/table/tbody/tr/td[2]/select', unique_tic_list_icao[index])

    # Send the airport codes to the ICAO calculator

    unique_scrape.send('frm1', unique_dep_list[index], unique_dep_city[index], '/html/body/ul[1]', 'li')
    unique_scrape.send('to1', unique_arr_list[index], unique_arr_city[index], '/html/body/ul[2]', 'li')

    # Compute emissions and extract the resulting number from the website

    print("Computing: " + str(index + 1) + " / " + str(len(unique_dep_list)) + " ...")
    unique_scrape.compute()
    table = unique_scrape.extract_from_table("/html/body/div[1]/form/div[2]/div/div/div[1]/div[1]/table/tbody/tr", "th")
    unique_emissions.append(table[6])

    # Clear departure and arrival inputs for next iteration

    unique_scrape.clear_inputs('frm1')
    unique_scrape.clear_inputs('to1')

    unique_csv = unique_scrape.append_to_csv(unique_emissions[index], index, 'Emissions')  # FIXME: does not include ICAO trip category column

# TODO: back-fill matches from unique calculations
# functions_new.fill_from_uniques(uniques_path, subset_path)

print("All done. Finished in: " + (time.time() - start_time) + "s.")