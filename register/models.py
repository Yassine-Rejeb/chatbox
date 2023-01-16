from django.db import models
import pymongo

def encryptPassword(password):
    # Hash a password with SHA256
    import hashlib
    hash_object = hashlib.sha256(password.encode())
    return hash_object.hexdigest()
class mongoConnection():
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://mongodb-server:27017/")
        self.db = self.client['chatbox']
        self.usersCollection = self.db['users']
        self.createSupportUserIfNotExists()
    def insert(self, username, password, email, verified):
        self.usersCollection.insert_one({'username': username, 'password': encryptPassword(password), 'email': email, 'verified': verified, 'friends': ["support"]})
        self.createSupportUserIfNotExists()
    def createSupportUserIfNotExists(self):
        if self.usersCollection.find({'username': 'support'}) == 0:
            self.usersCollection.insert_one({'username': 'support', 'password': encryptPassword('Rly5trongP4$sw0rd'), 'email': 'support@chatbox.tn', 'verified': True, 'friends': []})  
    def find(self, username, password):
        return self.usersCollection.find_one({'username': username, 'password': encryptPassword(password)})
    def findEmail(self, email):
        return self.usersCollection.find_one({'email': email})
    def findUsername(self, username):
        return self.usersCollection.find_one({'username': username})
    def findEmailWhenVerified(self, email):
        return self.usersCollection.find_one({'email': email, 'verified': True})
    def update(self, username, password, email):
        self.usersCollection.update_one({'username': username, 'password': encryptPassword(password), 'email': email})
    def delete(self, username, password, email):
        self.usersCollection.delete_one({'username': username, 'password': encryptPassword(password), 'email': email})
    def close(self):
        self.client.close()