# Import libraries, functions, and PyScraper class

from code.PyScraper import PyScraper

link = 'https://applications.icao.int/icec'
subset_path = 'data/concur_flights_working_data_subset.csv'
full_path = '/home/lucia/sustainability/ccl/code/employee-travel-emissions/scrapers/data/concur_flights_raw_data.csv'

subset_scrape = PyScraper(link, subset_path)
# print(subset_scrape.test_class())  # print test passed 1/8/21

# Get the departure and arrival airport codes
dep_list = subset_scrape.extract_column('Departure Station Code')
arr_list = subset_scrape.extract_column('Arrival Station Code')

# print('Departure codes: ')
# print(str(dep_list))  # print test passed 1/8/21
# print('Arrival codes: ')
# print(str(arr_list))  # print test passed 1/8/21

# Get the entries in the departure and arrival city columns
dep_loc = subset_scrape.extract_column('Departure City')
arr_loc = subset_scrape.extract_column('Arrival City')

# Parse the city names from these
dep_city = subset_scrape.parse_cities(dep_loc)
arr_city = subset_scrape.parse_cities(arr_loc)

print('Departure cities: ')
print(str(dep_city))  # print test passed 1/8/21
print('Arrival cities: ')
print(str(arr_city))  # print test passed 1/8/21

# Send the codes to the ICAO calculator

for index in range(len(dep_list)):
    subset_scrape.send('frm1', dep_list[index], dep_city[index], "/html/body/ul[1]", "li")

    # TODO: test the match function
    # TODO: work out in which order to send departure and arrival info to ICAO

