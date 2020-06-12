import pandas as pd
import boto3
client=boto3.client('s3')

'''Giving aws s3 bucket and csv file path'''
filepath='s3://myworkingbuckets/Stock_Price_Data.csv'

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


'''Renaming columns'''
df = df.rename(columns={df.columns[1] : 'Close'})
df = df.rename(columns={df.columns[2] : 'Volume'})
df = df.rename(columns={df.columns[3] : 'Open'})
df = df.rename(columns={df.columns[4] : 'High'})
df = df.rename(columns={df.columns[5] : 'Low'})

#print
(df.head(5))

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession

sc = SparkContext()
sparkSession = SparkSession(sc)
stock_price_data = sparkSession.createDataFrame(df)
#print(stock_price_data)

'''print(stock_price_data.cache())
print(stock_price_data.printSchema())
print(stock_price_data.describe().toPandas().transpose())
'''
try:
    selected_data=stock_price_data.select([' Open', ' High', ' Low', ' Close'])
except NameError:
    print("Invalid column name")


'''Prepare data for Machine Learning'''
from pyspark.ml.feature import VectorAssembler
vectorAssembler = VectorAssembler(inputCols=[' Open', ' High', ' Low'], outputCol='features')
vector_df= vectorAssembler.transform(selected_data)
vector_df = vector_df.select(['features', ' Close'])
#print(vector_df)


'''Spliting data into training and testing'''
splits = vector_df.randomSplit([0.7, 0.3])
train_df = splits[0]
test_df = splits[1]

'''Model Building'''
from pyspark.ml.regression import LinearRegression
LinearRegressor = LinearRegression(featuresCol = 'features', labelCol=' Close',
                maxIter=10, regParam=0.3)
linear_model = LinearRegressor.fit(train_df)
print("Coefficients: " + str(linear_model.coefficients))
print("Intercept: " + str(linear_model.intercept))


'''Testing Model'''
predictions = linear_model.transform(test_df)
predictions.select("prediction",' Close','features').show()

from pyspark.ml.evaluation import RegressionEvaluator
SummaryData = linear_model.summary
print("RMSE: %f" % SummaryData.rootMeanSquaredError)
print("r2: %f" % SummaryData.r2)

'''Saving Model'''
linear_model.save("stockmodel")
print("Succesfully Saved")

'''By using Pickle
import pickle
Pkl_Filename = "Pickle_LR_Model"
with open(Pkl_Filename, 'wb') as f:
    pickle.dump(linear_model, f)'''
