StockPricePrediction

The purpose of this project is to predict stock price using real time data. In this project I used past Google stock prices and built machine learning model using pyspark ml library and predicted stock price. I used alphavantage services, which allows to get real time stock prices. Predicted price is portrayed on web page using Flask on AWS EC2 instance.
Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
Prerequisites

    Download kafka
    Create api key on alphavantage

Installation

Install python package manager pip

sudo apt-get install python3-pip

Install required libraries from requirements.txt

pip3 install -r requirements.txt

Setup Environment

Add following to bashrc file

export PYSPARK_PYTHON=/usr/bin/python3
export PYSPARK_DRIVER_PYTHON=python3

Steps

    File to AWS S3
        Download historical stock data from nasdaq
        Create file aws_credentials with aws credentials
        Run script to create s3 bucket and upload file

    Train Model
        Copy aws sdk jars (i.e., hadoop-aws-2.7.7.jar, aws-java-sdk-1.7.4.jar from hadoop folder to spark jars folder
        Run script, check performance of model and save model

    Run Kafka Server In kafka directory run following commands to start zookeeper and kafka

    bin/zookeeper-server-start.sh config/zookeeper.properties

    bin/kafka-server-start.sh config/server.properties

    Run kafka producer
        live_data file consists of kafka producer which sends real time data from alpha vantage to kafka server

    Run app.py
        predict_live_data.py consists kafka consumer code that takes real time data then predicts the stock price and sends to web page

Deployment

    To deploy flask application, create EC2 instance with atleast 4 GB capacity RAM of ubuntu OS on AWS.
    Create http secuirty group to allow public to view web site.
    Download .pem file to access instance from local terminal.
    To access instance from local terminal, make ssh connection

ssh -i flask.pem ubuntu@<public IP address of ec2 instance>

    Now update packages

sudo apt-get update

    Install git

sudo apt-get install git

    Clone the project
    Install pip

sudo apt-get install python3-pip

    Now install required libraries

pip3 install -r requirements.txt

    Install Gunicorn3, it is a Python Web Server Gateway Interface HTTP server.

pip3 install gunicorn3

    Install nginx, Nginx is a web server which can also be used as a reverse proxy, load balancer, mail proxy and HTTP cache.

sudo apt-get install nginx

    Set up environment as above mentioned procedure
    Download kafka and run zookeeper and kafka server in backgroud

nohup bin/zookeeper-server-start.sh config/zookeeper.properties &

nohup bin/kafka-server-start.sh config/server.properties &

    Go to nginx sites-enabled directory

cd /etc/nginx/sites-enabled

    create new file

sudo nano flaskapp

    Configure following

server{
    listen 80;
    server_name <your ec2 instace public IP address>;
    
    location / {
          proxy_pass http://127.0.0.1:8000;
    }
}

    Now restart nginx server

sudo service nginx restart

    Go back to project directory
    Now run live_data.py file in background

nohup python3 live_data.py &

    You can check background nohup jobs by

jobs -l

    Remove if condition main in app.py to run server by gunicorn and run

gunicorn3 --threads=4 app:app

    else

gunicorn3 --threads=4 predict_live_data:app

    Here you will get http address that is visible publicly
