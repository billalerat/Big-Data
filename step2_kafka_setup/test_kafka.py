from kafka import KafkaProducer, KafkaConsumer
import json
import time

# Kafka connection details
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'test_topic'

def test_producer():
    # Create a producer
    producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER],
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    
    # Send test messages
    for i in range(5):
        message = {'number': i}
        producer.send(TOPIC_NAME, value=message)
        print(f'Sent: {message}')
        time.sleep(1)
    
    producer.flush()
    producer.close()

def test_consumer():
    # Create a consumer
    consumer = KafkaConsumer(TOPIC_NAME,
                             bootstrap_servers=[KAFKA_BROKER],
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='test_group',
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    
    # Read messages from the topic
    print('Consuming messages...')
    for message in consumer:
        print(f'Received: {message.value}')

if __name__ == '__main__':
    print("Testing Kafka Producer...")
    test_producer()
    print("Testing Kafka Consumer...")
    test_consumer()