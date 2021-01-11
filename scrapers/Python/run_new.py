# Import libraries, functions, and PyScraper class

from code.PyScraper import PyScraper
from code import functions_new
import pandas as pd
import time

link = 'https://applications.icao.int/icec'

# Data paths - edit as needed according to system
subset_path       = 'data/concur_flights_working_data_subset.csv'
full_path         = 'data/concur_flights_raw_data.csv'
compare_path      = 'data/emissions_compare.csv'
flight_types_path = 'data/flight_types.csv'
results_path      = 'output6_full.csv'  # replace w/ 'output5.csv' if testing on subset

print('Testing.')
# print(pd.read_csv('output6_full.csv')['Emissions'])
test_scrape = PyScraper(link, 'data/unique_trips_full.csv')

print(functions_new.index_of_next_calc('output6_full.csv'))  # first print test passed 1/11/21
print('No longer testing.')
quit()

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

# functions_new.fill_from_uniques(uniques_path, subset_path)

# TODO: extract unique trips into another data.csv -> compute emissions & print -> back-fill matches

print("All done. Finished in: " + (time.time() - start_time) + "s.")