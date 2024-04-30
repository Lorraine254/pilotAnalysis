# library 
library(umx)

# data
expectation_data <-read.csv('expectations.csv')
perception_data <-read.csv('perception.csv')

#read data
head(expectation_data)
head(perception_data)

# converting data into matrix
my_expectation <- data.matrix(expectation_data)
my_perception <- data.matrix(perception_data)

reliability(cov(my_perception))

reliability(cov(my_expectation))


