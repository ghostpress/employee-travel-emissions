# Read in the data:

dat_raw = read.csv("concur_flights_raw_data.csv", header = TRUE)

# Subsetting

years_of_interest <- 2017:2019 # ignoring 2020 for now
dat_years

for(yr in years_of_interest) {
  dat_years = subset(dat_raw, Departure_Date.contains(c(yr)))
}
