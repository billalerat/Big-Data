"""
Script de test de connexion à Kafka
"""

from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.admin import NewTopic
import json

BOOTSTRAP_SERVERS = ['localhost:9092']
TOPIC_NAME = 'blood-pressure-observations'

def test_connection():
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
        print("✅ Connexion Kafka réussie!")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def create_topic():
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
        topic = NewTopic(
            name=TOPIC_NAME,
            num_partitions=3,
            replication_factor=1
        )
        admin_client.create_topics(new_topics=[topic], validate_only=False)
        print(f"✅ Topic '{TOPIC_NAME}' créé!")
        return True
    except Exception as e:
        if "already exists" in str(e):
            print(f"⚠️  Topic '{TOPIC_NAME}' existe déjà")
            return True
        print(f"❌ Erreur: {e}")
        return False

def test_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        test_message = {
            "resourceType": "Observation",
            "id": "TEST-001",
            "status": "final",
            "component": [
                {"code": {"coding": [{"code": "8480-6"}]}, "valueQuantity": {"value": 120}},
                {"code": {"coding": [{"code": "8462-4"}]}, "valueQuantity": {"value": 80}}
            ]
        }
        
        producer.send(TOPIC_NAME, test_message)
        producer.flush()
        producer.close()
        print("✅ Message test envoyé!")
        return True
    except Exception as e:
        print(f"❌ Erreur Producer: {e}")
        return False

if __name__ == "__main__":
    print("\n🧪 TEST DE KAFKA\n")
    test_connection()
    create_topic()
    test_producer()
    print("\n✅ Tests terminés!\n")
