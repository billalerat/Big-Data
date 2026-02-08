# Test Kafka Connectivity

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable

def test_kafka_connectivity(broker_address):
    try:
        producer = KafkaProducer(bootstrap_servers=broker_address)
        consumer = KafkaConsumer('test_topic', bootstrap_servers=broker_address)
        producer.close()
        consumer.close()
        print("Kafka connection successful!")
    except NoBrokersAvailable:
        print("No Kafka brokers available!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    test_kafka_connectivity('localhost:9092')  # Change to your broker address