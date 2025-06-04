#Download the Kafka File
#wget https://archive.apache.org/dist/kafka/3.7.0/kafka_2.12-3.7.0.tgz

# unzip the file
# tar -xzf kafka_2.12-3.7.0.tgz

# CHANGE TO THE FILE DIRECTORY
#cd kafka_2.12-3.7.0

#Generate a Cluster UUID that will uniquely identify the Kafka Cluster
# KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"

# Configure the KRaft log directories
"""/home/carl/kafka_2.12-3.7.0/bin/kafka-storage.sh format \
 -t $KAFKA_CLUSTER_ID -c /home/carl/kafka_2.12-3.7.0/config/kraft/server.properties"""

#Start the Kafka Server
"""/home/carl/kafka_2.12-3.7.0/bin/kafka-server-start.sh \
/home/carl/kafka_2.12-3.7.0/config/kraft/server.properties"""


#STEP 2 STARTING A MYSQL SERVER AND SETUP DATABASE
#Start mysql
# sudo systemctl start mysql

#Connect to Mysql 
# sudo mysql -u root -p

#Create a Database tolldata
#CREATE DATABASE tolldata;

"""Depending on your LINUX environment mysql denies access to mysql connection without a super user permissions
#Therefore to connect to our database from our python-kafka broker we will create a new user
# and grant them full privilege to the specific database"""

#CREATE USER 'local_user' IDENTIFIED BY 'secure_password';
#GRANT ALL PRIVILEGES ON tolldata.* TO 'local_user';
#FLUSH PRIVILEGES;

# We will then Create a table in our database to store our streaming data
#USE tolldata;

#CREATE TABLE livetolldata(timestamp datetime,vehicle_id int,vehicle_type char(15),toll_plaza_id smallint);

#Exit from the database
#EXIT;

# 3 INSTALLING THE PYTHON PACKAGES
#To install python packages onto our Linux Environment We will need to create a virtual environment
#Select a new Linux Terminal & Switch to the kafka directory
#cd kafka_2.12-3.7.0

#Create a new virtual environment called venv installing python3
#python3 -m venv venv

#Activate the virtual environment
#source venv/bin/activate

#Install kafka-python
#pip3 install kafka-python

#Install Connector to mysql
#pip3 install mysql-connector-python==8.0.31

#Create python files to read our python commands for the producer data and consumer data
#Open the consumer file in a code editor and paste the following command
# The code generates random cars and streams them to the produce 
"""

#Top Traffic Simulator

from time import sleep, time, ctime
from random import random, randint, choice
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

#Define Your Topic
TOPIC = 'name_of_topic'

VEHICLE_TYPES = ("BMW", "car", "BMW", "car", "car", "car", "BMW", "car",
                 "car", "car", "car", "truck", "truck", "truck",
                 "truck", "van", "van")
#Generate Rnadom Choices from the Vehicle Types
for _ in range(100000):
    vehicle_id = randint(10000, 10000000)
    vehicle_type = choice(VEHICLE_TYPES)
    now = ctime(time())
    plaza_id = randint(4000, 4010)
    message = f"{now},{vehicle_id},{vehicle_type},{plaza_id}"
    message = bytearray(message.encode("utf-8"))
    print(f"A {vehicle_type} has passed by the toll plaza {plaza_id} at {now}.")
    producer.send(TOPIC, message)
    sleep(random() * 2)

"""
# Save the python file in you kafka directory
#Run the Python File in your virtual environment
#python3 producer_file.py
#You should see a stream of random cars generated from the code
# To interrupt the stream use COMMAND+C

#Open a new terminal and switch to the virtual environment
#Open the Consumer file
#We will first connect to the tolldata database
#We will the append the streaming data to a table in the database

"""

from datetime import datetime
from kafka import KafkaConsumer
import mysql.connector

TOPIC = 'toll'
DATABASE = 'tolldata'
USERNAME = 'user_name'
PASSWORD = 'password'

connection = None  # Initialize connection variable

print("Connecting to the database")
try:
    connection = mysql.connector.connect(
        host='localhost',  # ← use 'localhost' for local machine
        database=DATABASE,
        user=USERNAME,
        password=PASSWORD
    )
    cursor = connection.cursor()
    print("Connected to database")

except mysql.connector.Error as e:
    print("Could not connect to database. Error:", e)

if connection:
    print("Connecting to Kafka")
    consumer = KafkaConsumer(TOPIC)
    print("Connected to Kafka")
    print(f"Reading messages from the topic '{TOPIC}'")

    for msg in consumer:
        message = msg.value.decode("utf-8")
        (timestamp, vehicle_id, vehicle_type, plaza_id) = message.split(",")

        dateobj = datetime.strptime(timestamp, '%a %b %d %H:%M:%S %Y')
        timestamp = dateobj.strftime("%Y-%m-%d %H:%M:%S")

        sql = "INSERT INTO livetolldata VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (timestamp, vehicle_id, vehicle_type, plaza_id))
        connection.commit()
        print(f"A {vehicle_type} was inserted into the database.")

    connection.close()
else:
    print("Kafka consumer not started due to DB connection failure.")
"""

#Running the consumer file should generate a stream on the from the producer.







