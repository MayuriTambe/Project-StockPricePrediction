import pandas as pd
import boto3
client=boto3.client('s3')

'''Giving aws s3 bucket and csv file path'''
filepath=("/home/maya/Desktop/HistoricalQuotes.csv")

'''reading csv file'''
df=pd.read_csv(filepath)
#print(df)
# If error occurs then install s3fs by running !pip install s3fs



'''Checking null values in file'''
#print
(df.isnull().sum())

'''Converting data into datetime format'''
df['Date']=pd.to_datetime(df.Date)
df['Date']=df['Date'].dt.strftime('%m/%d/%Y')
#print(df)

'''Removing Dollar sign from the file'''
def remove_dollarsign():
    try:
        df[df.columns[1:]] = df[df.columns[1:]].replace('[\$,]', '', regex=True).astype(float)
    except ValueError:
        print("Could not convert data to an integer.")
remove_dollarsign()

'''Creating new filtered file from dataframe'''
print(df.to_csv("New-HistoricalQuotes.csv", index=False))