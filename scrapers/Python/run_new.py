# Import libraries, functions, and PyScraper class

from code.PyScraper import PyScraper

link = 'https://applications.icao.int/icec'

# Data paths - edit as needed according to system
subset_path       = 'data/concur_flights_working_data_subset.csv'
full_path         = 'data/concur_flights_raw_data.csv'
compare_path      = 'data/emissions_compare.csv'
flight_types_path = 'data/flight_types.csv'

subset_scrape = PyScraper(link, subset_path)

# Get the list of ticket classes
tic_list = subset_scrape.extract_column('Class of Service')

# Put the ticket class list into the correct categories for ICAO
tic_list_icao = subset_scrape.convert_tickets(tic_list, flight_types_path)

# Get the departure and arrival airport codes
dep_list = subset_scrape.extract_column('Departure Station Code')
arr_list = subset_scrape.extract_column('Arrival Station Code')

# Get the entries in the departure and arrival city columns
dep_loc = subset_scrape.extract_column('Departure City')
arr_loc = subset_scrape.extract_column('Arrival City')

# Parse the city names from these
dep_city = subset_scrape.parse_cities(dep_loc)
arr_city = subset_scrape.parse_cities(arr_loc)

emissions = []

for index in range(len(dep_list)):

    # Set the trip type (all one way)
    subset_scrape.set_trip_type('/html/body/div[1]/form/div[1]/div[1]/div/table/tbody/tr/td[1]/select', 'One Way')

    # Set the cabin class category
    subset_scrape.set_cabin_class('/html/body/div[1]/form/div[1]/div[1]/div/table/tbody/tr/td[2]/select', tic_list_icao[index])

    # Send the airport codes to the ICAO calculator

    subset_scrape.send('frm1', dep_list[index], dep_city[index], '/html/body/ul[1]', 'li')
    subset_scrape.send('to1', arr_list[index], arr_city[index], '/html/body/ul[2]', 'li')

    # Compute emissions and extract the resulting number from the website

    subset_scrape.compute()
    table = subset_scrape.extract_from_table("/html/body/div[1]/form/div[2]/div/div/div[1]/div[1]/table/tbody/tr", "th")
    emissions.append(table[6])

    # Clear departure and arrival inputs for next iteration

    subset_scrape.clear_inputs('frm1')
    subset_scrape.clear_inputs('to1')

    compare_csv = subset_scrape.append_to_csv(emissions[index], index, 'Emissions.Py')

# TODO: extract unique trips into another data.csv -> compute emissions & print -> back-fill matches

print("All done.")