"""
ÉTAPE 4 : Storage and Processing with MongoDB
Stores FHIR data from Kafka into MongoDB and performs aggregations

Auteur: Projet Big-Data
Date: 2026
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
import json
from datetime import datetime

# Configuration
MONGODB_URI = "mongodb://localhost:27017"
DATABASE_NAME = "blood_pressure_db"
COLLECTION_NAME = "observations"

class MongoDBStorage:
    """Store and manage FHIR observations in MongoDB"""
    
    def __init__(self, uri=MONGODB_URI):
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.server_info()
            self.db = self.client[DATABASE_NAME]
            self.collection = self.db[COLLECTION_NAME]
            print("✅ Connected to MongoDB")
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            raise
    
    def store_observation(self, observation):
        """Store a single FHIR observation"""
        try:
            # Add timestamp
            observation['stored_at'] = datetime.utcnow()
            
            # Insert or update
            result = self.collection.insert_one(observation)
            return {
                'success': True,
                'id': str(result.inserted_id)
            }
        except DuplicateKeyError:
            return {
                'success': False,
                'error': 'Observation already exists'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def store_batch(self, observations):
        """Store multiple observations"""
        results = []
        for obs in observations:
            result = self.store_observation(obs)
            results.append(result)
        return results
    
    def get_all_observations(self):
        """Retrieve all observations"""
        return list(self.collection.find({}, {'_id': 0}))
    
    def get_observation_by_id(self, obs_id):
        """Retrieve observation by ID"""
        return self.collection.find_one({'id': obs_id}, {'_id': 0})
    
    def get_observations_by_patient(self, patient_id):
        """Retrieve observations for a specific patient"""
        return list(self.collection.find(
            {'subject.reference': f'Patient/{patient_id}'},
            {'_id': 0}
        ))
    
    def aggregate_blood_pressure_stats(self):
        """Calculate blood pressure statistics"""
        pipeline = [
            {
                '$unwind': '$component'
            },
            {
                '$group': {
                    '_id': '$component.code.coding.0.code',
                    'avg_value': {'$avg': '$component.valueQuantity.value'},
                    'min_value': {'$min': '$component.valueQuantity.value'},
                    'max_value': {'$max': '$component.valueQuantity.value'},
                    'count': {'$sum': 1}
                }
            }
        ]
        return list(self.collection.aggregate(pipeline))
    
    def count_abnormal_readings(self):
        """Count observations with abnormal readings"""
        # This is a simplified example
        return self.collection.count_documents({})
    
    def create_indexes(self):
        """Create necessary indexes for performance"""
        self.collection.create_index('id', unique=True)
        self.collection.create_index('subject.reference')
        self.collection.create_index('stored_at')
    
    def delete_all(self):
        """Delete all observations (for testing)"""
        result = self.collection.delete_many({})
        return result.deleted_count
    
    def close(self):
        """Close MongoDB connection"""
        self.client.close()

# Example usage
if __name__ == "__main__":
    print("\n" + "="*60)
    print("💾 ÉTAPE 4 : STORAGE WITH MONGODB")
    print("="*60 + "\n")
    
    storage = MongoDBStorage()
    
    # Create indexes
    storage.create_indexes()
    
    # Example observations
    observations = [
        {
            "id": "OBS-001",
            "resourceType": "Observation",
            "status": "final",
            "subject": {"reference": "Patient/PAT-001"},
            "effectiveDateTime": "2026-02-08T10:00:00Z",
            "component": [
                {"code": {"coding": [{"code": "8480-6", "display": "Systolic"}]}, "valueQuantity": {"value": 120}},
                {"code": {"coding": [{"code": "8462-4", "display": "Diastolic"}]}, "valueQuantity": {"value": 80}}
            ]
        },
        {
            "id": "OBS-002",
            "resourceType": "Observation",
            "status": "final",
            "subject": {"reference": "Patient/PAT-002"},
            "effectiveDateTime": "2026-02-08T11:00:00Z",
            "component": [
                {"code": {"coding": [{"code": "8480-6", "display": "Systolic"}]}, "valueQuantity": {"value": 140}},
                {"code": {"coding": [{"code": "8462-4", "display": "Diastolic"}]}, "valueQuantity": {"value": 90}}
            ]
        }
    ]
    
    # Store observations
    print("📥 Storing observations...\n")
    results = storage.store_batch(observations)
    
    successful = sum(1 for r in results if r.get('success'))
    print(f"✅ {successful}/{len(observations)} observations stored\n")
    
    # Get statistics
    print("📊 Blood Pressure Statistics:")
    stats = storage.aggregate_blood_pressure_stats()
    for stat in stats:
        print(f"  Code {stat['_id']}: Avg={stat['avg_value']:.1f}, "
              f"Min={stat['min_value']}, Max={stat['max_value']}, Count={stat['count']}")
    
    storage.close()
    print("\n" + "="*60 + "\n")
