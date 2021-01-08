# Import libraries, functions, and PyScraper class

from code.PyScraper import PyScraper

link = 'https://applications.icao.int/icec'
subset_path = 'data/concur_flights_working_data_subset.csv'
full_path = '/home/lucia/sustainability/ccl/code/employee-travel-emissions/scrapers/data/concur_flights_raw_data.csv'

# Testing

# test_scrape = PyScraper(link, subset_path)
# dep = 'BOS'
# arr = 'DCA'
# test_scrape.send('frm1', dep, 'Boston', '/html/body/ul[1]', 'li')
# test_scrape.send('to1', arr, 'Washington', '/html/body/ul[2]', 'li')

subset_scrape = PyScraper(link, subset_path)

# Get the departure and arrival airport codes
dep_list = subset_scrape.extract_column('Departure Station Code')
arr_list = subset_scrape.extract_column('Arrival Station Code')

# Get the entries in the departure and arrival city columns
dep_loc = subset_scrape.extract_column('Departure City')
arr_loc = subset_scrape.extract_column('Arrival City')

# Parse the city names from these
dep_city = subset_scrape.parse_cities(dep_loc)
arr_city = subset_scrape.parse_cities(arr_loc)

for index in range(len(dep_list)):

    # Send the codes to the ICAO calculator

    subset_scrape.set_trip_type("/html/body/div[1]/form/div[1]/div[1]/div/table/tbody/tr/td[1]/select", "One Way")
    subset_scrape.send('frm1', dep_list[index], dep_city[index], '/html/body/ul[1]', 'li')
    subset_scrape.send('to1', arr_list[index], arr_city[index], '/html/body/ul[2]', 'li')

    # Compute emissions and extract the resulting number from the website

    emissions = []
    subset_scrape.compute("computeByInput")
    table = subset_scrape.extract_from_table("/html/body/div[1]/form/div[2]/div/div/div[1]/div[1]/table/tbody/tr", "th")
    emissions.append(table[6])
    print(emissions)

    # Clear departure and arrival inputs for next iteration

    subset_scrape.clear_inputs('frm1')
    subset_scrape.clear_inputs('to1')

# print(emissions)

# Add a column with the emissions to the csv
subset_scrape.append_to_csv(emissions)  # TODO: actually append to a CSV rather than df, to prevent loss in case of crash

# for index in range(len(dep_list)):
#     subset_scrape.send('frm1', dep_list[index], dep_city[index], "/html/body/ul[1]", "li")

