"""
ÉTAPE 4 : Consumer Kafka to MongoDB
Consumes messages from Kafka and stores them in MongoDB
"""

from kafka import KafkaConsumer
from storage import MongoDBStorage
import json

# Configuration
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
KAFKA_TOPIC = 'blood-pressure-observations'
KAFKA_GROUP_ID = 'mongodb-consumer-group'

class KafkaToMongoDBConsumer:
    """Consumer that reads from Kafka and writes to MongoDB"""
    
    def __init__(self, mongo_db_name, mongo_collection_name):
        self.consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id=KAFKA_GROUP_ID,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        self.storage = MongoDBStorage(mongo_db_name, mongo_collection_name)
    
    def consume_and_store(self, max_messages=None):
        """Consume messages and store in MongoDB"""
        print("\n" + "="*60)
        print("📥 KAFKA TO MONGODB CONSUMER")
        print("="*60 + "\n")
        
        message_count = 0
        stored_count = 0
        
        try:
            for message in self.consumer:
                message_count += 1
                
                observation = message.value
                
                # Store in MongoDB
                result = self.storage.insert_observation(observation)
                stored_count += 1
                
                print(f"[{message_count}] Stored observation {observation.get('id')} - \
                      f"MongoDB ID: {result.inserted_id}")
                
                if max_messages and message_count >= max_messages:
                    break
        
        except KeyboardInterrupt:
            print("\n⏸️ Consumer stopped")
        
        finally:
            self.storage.close()
        
        print(f"\n✅ {stored_count} observations stored in MongoDB")
        print("="*60 + "\n")

if __name__ == "__main__":
    consumer = KafkaToMongoDBConsumer('blood_pressure_db', 'observations')
    consumer.consume_and_store()