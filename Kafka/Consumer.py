import json
import time
import pandas as pd
import os

from datetime import datetime
#from flask import Flask, render_template, make_response

from pyspark import SparkContext
from pyspark.shell import sqlContext
from pyspark.sql import SQLContext
from kafka import KafkaConsumer
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegressionModel, SparkSession
from pyspark.sql.types import DoubleType
sc = SparkContext.getOrCreate()
sparkSession = SparkSession(sc)

#os.environ["PYSPARK_PYTHON"]="python3"
#os.environ["PYSPARK_DRIVER_PYTHON"]="python3"

from pyspark.ml.feature import VectorAssembler
vectorAssembler = VectorAssembler(inputCols=[' Open', ' High', ' Low'], outputCol='features')
load_model = LinearRegressionModel.load("stockmodel")
print("Model loaded successfully")
consumer  = KafkaConsumer('stock')
def stock_prediction(load_model):
    consumer  = KafkaConsumer('stock')
    for message in consumer:
    #print(type(message.value))
        #loading input data in json format
        loaddata = json.loads(message.value.decode('utf-8'))
        data = list(loaddata.values())
        dataframe = pd.DataFrame([data], columns=['Open','Close','Volume','High','Low'])
        #creating dataframe using sparkContext
        spark_df = sqlContext.createDataFrame(dataframe)
        #convering data from all columns into double data type by using spark cast() function
        try:
            spark_df = spark_df.selectExpr("cast(Volume as double)Volume",
                                                     "cast(Open as double)Open",
                                                     "cast(Low as double)Low",
                                                     "cast(High as double)High",
                                                     "cast(Close as double)Close")
        except:
            print("column does not exists")

        #splitting data into inputcolumns and outputcolumns
        vectorAssembler = VectorAssembler(inputCols = ['Open','High','Low'], outputCol = 'features')
        vectored_df = vectorAssembler.transform(spark_df)
        features_results = vectored_df.select(['features','Close'])

        #Prediction of new stock data with out train model
        predictions = load_model.transform(features_results)
        predictions.select("prediction","Close","features").show()
        predict_value = predictions.select('prediction').collect()[0].__getitem__("prediction")
        close_data = predictions.select('Close').collect()[0].__getitem__('Close')
        print(message.key)

        datetimevalue = message.key.decode('utf-8')
        return predict_value , close_data , datetimevalue

stock_prediction(load_model)