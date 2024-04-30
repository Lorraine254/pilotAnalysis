import pandas as pd

class DataSummarizer:
    """
    A class to store encoded data, encoding dictionary, 
    and descriptive analysis functions.
    """
    def __init__(self, df):
        self.df = df
        self.encodedDict = {}
        self.summary = {}

    def summaryOfData(self):
        print("----------------------------------------")  
        print("Statistical Summary of data")
        print(self.df.describe())
        print("----------------------------------------") 

    def dataUnderstanding(self):
        #structure of data
        print("---------------------------------------")
        print("         OVERVIEW OF DATA                ")
        print("---------------------------------------") 
        dimensions = self.df.shape 
        print(f"Data has  {dimensions[0]} records and  {dimensions[1]} features/variables.")
        print("----------------------------------------")
        df_types =  self.df.dtypes.value_counts()
        print(f"Data is composed of records, of nature:  {df_types}.")
        print("----------------------------------------")
        return self.df

    # dropping columns - general with axis 1
    def dropColumns(self, columns):
        self.df = self.df.drop(columns=columns, axis=1)
        return self.df

    # checking null values
    def checkNullValues(self):
        print("----------------------------------------")  
        print("Null Values Present in Data(%)")
        missing = pd.DataFrame(self.df.isna().sum() * 100 / len(self.df))   
        print(missing)   
        print("----------------------------------------")

    # encode and update the encofing dictionary with encoded categories
    def encodeCategoricalColumns(self):
        for col in self.df.select_dtypes(include=['object']):
            if(col != 'What is the most important reason for your score above?' and col != 'Timestamp'):
                self.df, self.encodedDict = self.encodingOfColumns(col)
    
    def encodingOfColumns(self, columnName):
        # check column data type if object convert to categorical
        if(self.df[columnName].dtype =='object'):
            # convert to categorical
            self.df[columnName] = self.df[columnName].astype('category')
        # attain number of unique elements - assuming the order will not be constant we take up a deterministic approach by embracing the .unique() method
            uniqueValues = self.df[columnName].unique()
        # assign/encode each a categorical value with a numerial value starting from 0 
            labelMapping = {v: i for i, v in enumerate(uniqueValues)}
            self.df[columnName] = self.df[columnName].replace(labelMapping)
        # populate an encoding dictionary in order of the columns
            self.encodedDict[columnName] = labelMapping
            # return df
        return self.df, self.encodedDict

    def generateSummaryFile(self, fileName, summary):
         # generate(summary,'FeatureDescriptiveSummary')
        with open(fileName, 'w') as f:
            # Column headers (adjust column widths as needed)
            f.write(f"| Column Name | Most Frequent Value | Percentage | Missing Values |\n")
            f.write("|" + "-" * 63 + "|\n")  # Separator line

            for col, info in summary.items():
                # Extract relevant information
                mostFrequentValue = info["Most Frequent Value"]
                percentage = info["Percentage"]
                missing_values = info["Missing Values"]

                # Format and write data (adjust formatting if needed)
                f.write(f" COLUMN: {col:<20} \n MOST FREQUENT VALUE: {mostFrequentValue:<20} \n PERCENTAGE: {percentage:<15} \n  MISSING VALUES:{missing_values:<15} |\n")
                f.write("|" + "-" * 63 + "|\n")  # Separator line

    # perfoming column based summary
    def getColumnSummary(self):
        """
        Provides a summary of each column in the DataFrame, including data type, missing values, most frequent value (percentage), and highlights if encoded.
        Returns:
            A dictionary containing summary information for each column.
        """
        summary = {}
        for col in self.df.columns:
            info = {
                "Data Type": self.df[col].dtype,
                "Missing Values": self.df[col].isna().sum()
            }
            mostFrequentInfo = self.getMostFrequentPercentage(col)
            info.update(mostFrequentInfo)  # Add most frequent info to the dictionary
            self.summary[col] = info
        # return summary
    
    def getMostFrequentPercentage(self, col):
        if self.df[col].dtype == 'object':
            # For categorical columns, use value_counts
            valueCounts = self.df[col].value_counts(normalize=True) * 100  # Calculate percentage
            mostFrequentValue = valueCounts.idxmax()
            mostFrequentPercentage = valueCounts.max()

            # Check if encoded (based on the presence in encodingDict)
            encoded = col in self.encodedDict

            # Decode if encoded
            if encoded:
                decodedValue = self.encodedDict[col][mostFrequentPercentage]
                mostFrequentValue = decodedValue

            return {
                "Most Frequent Value": mostFrequentValue,
                "Percentage": f"{mostFrequentPercentage:.2f}%",
                "Encoded": encoded
            }
        else:
            # For numerical columns, use mode
            most_frequent_value = self.df[col].mode().iloc[0]  # Assuming single most frequent value
            return {
                "Most Frequent Value": most_frequent_value,
                "Percentage": "N/A%",  # Percentage not applicable for numerical data
                "Encoded": False
            }

        return None  # Handle potential errors (optional)
    
   
