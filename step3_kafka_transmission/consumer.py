# Kafka Consumer Script

from kafka import KafkaConsumer

# Replace 'your_topic' and 'your_broker' with actual values

def main():
    consumer = KafkaConsumer(
        'your_topic',
        bootstrap_servers=['your_broker'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: x.decode('utf-8')
    )
    
    for message in consumer:
        print(f'Consumed message: {message.value}')

if __name__ == '__main__':
    main()