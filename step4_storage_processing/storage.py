from pymongo import MongoClient

class MongoDBStorage:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def insert_observation(self, observation):
        """Insert a new FHIR observation into the database."""
        result = self.db.observations.insert_one(observation)
        return str(result.inserted_id)

    def get_observation(self, observation_id):
        """Retrieve a FHIR observation by ID."""
        observation = self.db.observations.find_one({"_id": observation_id})
        return observation

    def close(self):
        """Close the database connection."""
        self.client.close()