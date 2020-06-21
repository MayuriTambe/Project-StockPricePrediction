# StockPricePrediction
The Project based on Google Stock Price on real time value.In this project by using stock price data and built machine learning Linear Regression model and display data on web page using flask web application and deploy my model on AWS instance

**Requirements:**

- Create AWS account and Access keys 

- Download kafka

- Create api key on alphavantage site

- Install Flask
Steps:
   
**1.Uplaod csv file into AWS s3 bucket**

  - Download historical stock data from nasdaq
  - Create AWS account and s3 services 
  - Create aws_credential file containing all access keys with aws configure
  - Create and run Python script for creating s3 buckets and upload csv file in it

**2..Build and Train  model**

- Prepare data for machine learning model by applying data pre-processing on file
- Run Python script and check predicted value and save model

**3 .Run kafka and zookeeper server using following command in kafka directory**

```./bin/zookeeper-server-start.sh config/zookeeper.properties```

```./bin/kafka-server-start.sh config/server.properties```

 ```./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic <topicname>```
 
 ```./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic <topicname>```
    
 **4.Create and run kafka Producer python script**
 
  - Kafka Producer sends live data from alphavantage site to kafka server 
  - Create and run consumer python script
  - Kafka consumer gets data from producer through topics(stream of message) 
  
 **5.Create and run app.py file**
  - Consumer.py  script takes live data then predicts stock price and send to web page using flask
  - Cosisting index.html file for the graphical representation of Actual value and Predicted value
  - Create templates folder and stored index.html file in it
  - Pass consumer.py stock function in app.py file to  get predicted values
  - Output will display in browser 
  
 **6 Deployement Of Project:**
 
 1.Create EC2 instance
   - Create EC2 instance with Ubuntu Server 18.04 LTS as an AMI (Amazon Machine Image).and launch instance
   - Choose an Instance Type based on your requirement for better performance choose t2 medium and increased size of storage
   - Create a new security group named as flask-application and we will keep port 22 open by default to SSH into the instance and launch it.After that create a new key pair and given Key pair name as a flask and download key-pair and named as flask.pem
 
 2.SSH into EC2 instance
 
   - Require .pem (flask.pem) file or the private file to log in or SSH into our EC2 instance and hostname, that is nothing but the Public IP address (IPv4) attached to our instance.
   - Before we try to access the instance, we need to change the permission of pem file
chmod 400 flask.pem

```ssh -i flask.pem ubuntu@ipv4_address```
  
 3 .Configure EC2 instance for flask – Flask application with following commands

```sudo apt-get update```

```sudo apt-get install git```

```python3 -V```

```sudo apt install python3-pip```

```sudo apt-get install nginx```

```sudo apt-get install gunicorn3```

```pip3 install flask```



  4.Create directory for Project and clone your git repository

```mkdir Project```
   
```cd Project```
   
```git clone <repository_name>.git``` 
   
       

  5 Download kafka and run zookeeper and kafka server        

```nohup bin/zookeeper-server-start.sh config/zookeeper.properties &```

```nohup bin/kafka-server-start.sh config/server.properties &```


  6 Create flask app & configure nginx – Flask application

```cd /etc/nginx/sites-enabled```

```sudo nano flaskapp```

Configure following

 ```
 server{
    listen 80;
    server_name <your ec2 instace public IP address>;
    
    location / {
          proxy_pass http://127.0.0.1:8000;
    }
}
```

  7.Restart nginx server

```sudo service nginx restart```


  8.Run Project

```cd Project```

```python3 Producer.py```

```gunicorn3 --threads=4 app:app```


   
  9.Displaying output in web

```<Enstance_ip>:8080```

 

