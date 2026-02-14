# MongoDB Storage for FHIR Observations

import pymongo
from pymongo import MongoClient

class FHIRObservationStorage:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db['observations']

    def store_observation(self, observation):
        """
        Store a FHIR observation in the MongoDB collection.
        observation: dict -- The FHIR observation document to store.
        """
        self.collection.insert_one(observation)

    def retrieve_observations(self):
        """
        Retrieve all FHIR observations from the MongoDB collection.
        return: list -- List of observations.
        """
        return list(self.collection.find({}))

    def aggregate_blood_pressure(self):
        """
        Aggregate blood pressure data based on systolic and diastolic values.
        return: dict -- Aggregated blood pressure data with average values.
        """
        pipeline = [
            {
                '$match': {'code': {'$regex': 'blood pressure', '$options': 'i'}}
            },
            {
                '$group': {
                    '_id': None,
                    'avg_systolic': {'$avg': '$systolic'},
                    'avg_diastolic': {'$avg': '$diastolic'}
                }
            }
        ]
        result = self.collection.aggregate(pipeline)
        return list(result)
