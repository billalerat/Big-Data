# test_kafka.py

import kafka
from kafka import KafkaConsumer

# Define the Kafka server details
KAFKA_SERVER = 'localhost:9092'

# Create a consumer
consumer = KafkaConsumer(
    'test-topic',  # replace with your topic
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='test-group'
)

# Test Kafka connectivity
try:
    for message in consumer:
        print(f'Received message: {message.value}')
except Exception as e:
    print(f'Error occurred: {e}')
finally:
    consumer.close()