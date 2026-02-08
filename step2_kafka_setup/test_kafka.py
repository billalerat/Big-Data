import time
from kafka import KafkaProducer, KafkaConsumer

# Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'test-topic'

# Function to test Kafka producer

def test_kafka_producer():
    try:
        producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
        producer.send(TOPIC_NAME, b'Test message')
        producer.flush()
        print("Producer: Message sent successfully!")
    except Exception as e:
        print(f"Producer: Error sending message - {e}")

# Function to test Kafka consumer

def test_kafka_consumer():
    try:
        consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_BROKER)
        for message in consumer:
            print(f"Consumer: Received message: {message.value.decode()}")
            break  # Receive a single message for testing
    except Exception as e:
        print(f"Consumer: Error receiving message - {e}")


if __name__ == '__main__':
    test_kafka_producer()
    time.sleep(1)  # Wait for a moment before consuming
    test_kafka_consumer()