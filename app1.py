from kafka import KafkaConsumer
from json import loads
from pymongo import MongoClient

TOPIC = 'Blocks'
PARTITION_1 = 1

# Create the KafkaConsumer for partition 1
consumer = KafkaConsumer(TOPIC,
                         bootstrap_servers=['localhost:9092'],
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         value_deserializer=lambda x: loads(x.decode('utf-8')))

# Create the connection to MongoDB
CONNECTION_STRING = "mongodb://localhost:27017"

# Create a connection using MongoClient
mongo_client = MongoClient(CONNECTION_STRING)
itc6107_db = mongo_client['ITC6107']

# Access the database and get a reference to collection "Blocks"
blocks_collection = itc6107_db['Blocks']

for message in consumer:
    if message.partition == PARTITION_1:
        block = message.value
        print('Received Block from Kafka (Partition 1):', block)
        blocks_collection.insert_one(block)
