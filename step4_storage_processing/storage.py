import pymongo

class MongoDBStorage:
    def __init__(self, uri, database):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[database]

    def store_observation(self, observation):
        """Store an observation in the MongoDB database."""
        return self.db.observations.insert_one(observation)

    def retrieve_observation(self, observation_id):
        """Retrieve an observation by its ID."""
        return self.db.observations.find_one({'_id': observation_id})

    def aggregate_observations(self, pipeline):
        """Aggregate observations based on the provided pipeline."""
        return list(self.db.observations.aggregate(pipeline))

# Example usage:
# storage = MongoDBStorage('mongodb://localhost:27017/', 'fhir_database')
# storage.store_observation({'name': 'Blood Pressure', 'value': 120})
# observation = storage.retrieve_observation(some_id)
# aggregation_result = storage.aggregate_observations([{ '$group': { '_id': '$name', 'avg_value': { '$avg': '$value' } }}])
