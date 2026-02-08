import time
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.errors import KafkaError

# Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'test_topic'

# Function to test Kafka Producer

def test_producer():
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
    try:
        future = producer.send(TOPIC_NAME, key=b'test_key', value=b'test_value')
        record_metadata = future.get(timeout=10)  # wait until it is sent
        print(f'Produced to {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}')
    except KafkaError as e:
        print(f'Error producing message: {e}')
    finally:
        producer.close()

# Function to test Kafka Consumer

def test_consumer():
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='test_group'
    )
    for message in consumer:
        print(f'Consumed message: {message.value} from topic {message.topic}')

# Function to test topic creation

def test_topic_creation():
    admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
    try:
        admin_client.create_topics([TOPIC_NAME])
        print(f'Topic {TOPIC_NAME} created successfully.')
    except Exception as e:
        print(f'Error creating topic: {e}')

# Testing
if __name__ == '__main__':
    test_topic_creation()
    time.sleep(5)  # Ensure the topic is created before producing
    test_producer()
    test_consumer()