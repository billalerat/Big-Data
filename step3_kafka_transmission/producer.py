import kafka

class KafkaProducer:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.producer = kafka.KafkaProducer(bootstrap_servers=bootstrap_servers)

    def send_message(self, topic, message):
        self.producer.send(topic, value=message.encode('utf-8'))
        self.producer.flush()

if __name__ == '__main__':
    producer = KafkaProducer()
    producer.send_message('my_topic', 'Hello, Kafka!')