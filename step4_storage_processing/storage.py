# MongoDB Storage for FHIR Observations

"""
This module provides functions to store FHIR observations in a MongoDB database.
"""

from pymongo import MongoClient

class MongoDBStorage:
    """
    A class to manage storage of FHIR observations in MongoDB.
    """
    def __init__(self, db_name, collection_name):
        self.client = MongoClient()
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_observation(self, observation):
        """
        Insert a FHIR observation into the database.
        :param observation: A dictionary containing the observation data.
        """
        return self.collection.insert_one(observation)

    def find_observations(self, query):
        """
        Find observations in the database based on a query.
        :param query: A dictionary representing the query criteria.
        """
        return self.collection.find(query)

    def close(self):
        """
        Close the MongoDB connection.
        """
        self.client.close()