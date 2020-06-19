from time import sleep
from kafka import KafkaProducer
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import sys
import random
import json
from json import dumps
import time
from kafka.errors import KafkaError

#Extracting data from Google by using alphavantage API key
def fetch_data():
        ticker = 'GOOGL'
        lines = open('keys').read().splitlines()
        keys = random.choice(lines)
        time = TimeSeries(key=keys, output_format='json')
        data, metadata = time.get_intraday(symbol=ticker, interval="1min", outputsize='full')
        return data


#Reading data in json format and displaying message
def handle_message(producer_instance,key,data_key):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        producer_instance.send("stock",json.dumps(data[key]).encode('utf-8'),key_bytes)
        print("Displaying message")
    except Exception:
        print("Exception in Displaying message")

#Connecting kafka producer to getting live data
def connect_kafka_producer():

        try:
            producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        except KafkaError as err:
            print("Connection not established")
        return producer

if __name__ == "__main__":
        data = fetch_data()
        if (len(data) > 0):
            kafka_producer = connect_kafka_producer()
            for key in sorted(data):
                handle_message(kafka_producer, key, data[key])
                time.sleep(3)

