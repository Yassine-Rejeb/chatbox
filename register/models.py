from django.db import models
import pymongo
class mongoConnection():
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client['chatbox']
        self.usersCollection = self.db['users']
    def insert(self, username, password, email, verified):
        self.usersCollection.insert_one({'username': username, 'password': password, 'email': email, 'verified': verified})
    def find(self, username, password):
        return self.usersCollection.find_one({'username': username, 'password': password})
    def findEmail(self, email):
        return self.usersCollection.find_one({'email': email})
    def findUsername(self, username):
        return self.usersCollection.find_one({'username': username})
    def findEmailWhenVerified(self, email):
        return self.usersCollection.find_one({'email': email, 'verified': True})
    def update(self, username, password, email):
        self.usersCollection.update_one({'username': username, 'password': password, 'email': email})
    def delete(self, username, password, email):
        self.usersCollection.delete_one({'username': username, 'password': password, 'email': email})
    