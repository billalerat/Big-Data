class MongoDBStorage:
    def __init__(self, db_name, collection_name):
        from pymongo import MongoClient
        self.client = MongoClient()
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_observation(self, observation):
        self.collection.insert_one(observation)

    def find_observation(self, observation_id):
        return self.collection.find_one({'id': observation_id})

    def update_observation(self, observation_id, updated_data):
        self.collection.update_one({'id': observation_id}, {'$set': updated_data})

    def delete_observation(self, observation_id):
        self.collection.delete_one({'id': observation_id})
