from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import time
import json

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'test_topic'

# Function to test Kafka connection

def test_connection():
    try:
        producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
        producer.close()
        print('Kafka connection successful.')
    except Exception as e:
        print(f'Error connecting to Kafka: {e}')

# Function to create topic

def create_topic():
    from kafka.admin import KafkaAdminClient, NewTopic
    admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
    topic = NewTopic(name=TOPIC_NAME, num_partitions=1, replication_factor=1)
    admin_client.create_topics([topic])
    print(f'Topic {TOPIC_NAME} created successfully.')

# Function to test producer

def test_producer():
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
    for i in range(5):
        message = json.dumps({'number': i}).encode('utf-8')
        producer.send(TOPIC_NAME, value=message)
        print(f'Sent: {message}')
        time.sleep(1)  # Sleep for a bit before sending the next message
    producer.close()

# Function to test consumer

def test_consumer():
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_BROKER, auto_offset_reset='earliest')
    for message in consumer:
        print(f'Received: {message.value.decode()}')
        time.sleep(1)  # Process messages one by one

if __name__ == '__main__':
    test_connection()
    create_topic()
    test_producer()
    test_consumer()