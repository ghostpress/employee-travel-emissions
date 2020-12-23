setwd('./bu/sustainability/ccl/code/employee-travel-emissions/clean')

# Read in the data:

datRaw <- read.csv("concur_flights_raw_data.csv", header = TRUE)
datRawFrame <- data.frame(datRaw)
print(datRawFrame)

# Column names got shifted down into values, new column names are "X", "X.1", ..., "X.19"
# Rename these & remove the incorrectly formatted rows:

newColNames <- datRawFrame[2,]
print(newColNames)

for(i in 1:19) {
  
}