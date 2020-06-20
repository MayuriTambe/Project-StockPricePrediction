from pyspark import SparkContext
from pyspark.sql import SQLContext
from kafka import KafkaConsumer
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegressionModel
import os
import json
import pandas as pd

#os.environ["SPARK_HOME"] = "/usr/local/spark"
os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"

#Creating SparkContext
sc = SparkContext.getOrCreate()
sql=SQLContext(sc)
# Loading Model
model=LinearRegressionModel.load("stockmodel")

#Load and Read data by passing topic name as stock

def stock_prediction():
    consumer=KafkaConsumer('stock')
    for message in consumer:
        loaddata=json.loads(message.value.decode('utf-8'))
        data=list(loaddata.values())
        # print(data)
        dataframe=pd.DataFrame([data],columns=['Open','Close','Volume','High','Low'])
        # Create a data frame with Pandas
        sparkdf=sql.createDataFrame(dataframe)

        # convering data from all columns into double data type by using spark cast() function
        sparkFrame=sparkdf.selectExpr("cast(Open as double) Open",
                                        "cast(Close as double) Close",
                                        "cast(Volume as double) Volume",
                                        "cast(High as double) High",
                                        "cast(Low as double) Low")

        # splitting data into inputcolumns and outputcolumns
        vectorAssembler=VectorAssembler(inputCols=['Open','High','Low'],outputCol='features')
        # function to spliting input and output as supervised
        vectored_df=vectorAssembler.transform(sparkFrame)
        Feature_output=vectored_df.select(['features','Close'])

        # Prediction of stock data with out train model
        predictions=model.transform(Feature_output)
        # predict the new stock value with train model
        predictions.select("prediction","Close","features").show()
        # show the prediction data
        prediction_value=predictions.select('prediction').collect()[0].__getitem__("prediction")
        close_data=predictions.select('Close').collect()[0].__getitem__('Close')
        print(message.key)
        date_time=message.key.decode('utf-8')

        return prediction_value, close_data, date_time

stock_prediction()
