from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# Set up Kafka consumer
consumer = KafkaConsumer(
    'your_topic',  # replace with your Kafka topic
    bootstrap_servers=['your_kafka_server:9092'],  # replace with your Kafka server
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='your_group_id'
)

# Set up MongoDB client
mongo_client = MongoClient('mongodb://your_mongo_server:27017/')  # replace with your MongoDB server
mongo_db = mongo_client['your_database']  # replace with your database name
mongo_collection = mongo_db['your_collection']  # replace with your collection name

# Consume messages from Kafka and store them in MongoDB
for message in consumer:
    # Decode the message
    message_value = json.loads(message.value.decode('utf-8'))
    # Store the message in MongoDB
    mongo_collection.insert_one(message_value)
    print('Stored message in MongoDB:', message_value)