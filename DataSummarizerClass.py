import pandas as pd

class DataSummarizer:
    """
    A class to store encoded data, encoding dictionary, 
    and descriptive analysis functions.
    """
    def __init__(self, df):
        self.df = df
        self.encodedDict = {}

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
                self.df, self.encodingDict = self.encodingOfColumns(col)
    
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
