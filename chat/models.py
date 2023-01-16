import json
from django.db import models
import pymongo
from bson.json_util import dumps

# Create your models here

class image(models.Model):
    img = models.ImageField(upload_to='images/', default='images/default.png')

    def __str__(self):
        return self.img.name

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
        self.msgCollection = self.db['messages']
    
    def createSupportUserIfNotExists(self):
        if self.usersCollection.find_one({'username': 'support'}) == 0:
            self.usersCollection.insert_one({'username': 'support', 'password': encryptPassword('Rly5trongP4$sw0rd'), 'email': 'support@chatbox.tn', 'verified': True, 'friends': []})  

    def insert(self, username, password, email, verified):
        self.usersCollection.insert_one({'username': username, 'password': encryptPassword(password), 'email': email, 'verified': verified, 'friends': ["support"], 'requests_sent' : [], 'requests_received' : []})
        self.createSupportUserIfNotExists()

    def find(self, username, password):
        return self.usersCollection.find_one({'username': username, 'password': password})
    
    def findEmail(self, email):
        return self.usersCollection.find_one({'email': email})
    
    def findPassword(self, username):
        return self.usersCollection.find_one({'username': username})["password"] 

    def findUsername(self, username):
        return self.usersCollection.find_one({'username': username})
    
    def findEmailWhenVerified(self, email):
        return self.usersCollection.find_one({'email': email, 'verified': True})
    
    def findFriends(self, username):
        return self.usersCollection.find_one({'username': username})["friends"]
    
    def findFriend(self, username, friend):
        return self.usersCollection.find_one({'username': username, 'friends': friend})

    def update(self, username, password, email):
        self.usersCollection.update_one({'username': username, 'password': encryptPassword(password), 'email': email})
    
    def delete(self, username, password, email):
        self.usersCollection.delete_one({'username': username, 'password': encryptPassword(password), 'email': email})  
    
    def addFriend(self, username, friend):
        self.usersCollection.update_one({'username': username}, {'$push': {'friends': friend}})
        self.usersCollection.update_one({'username': friend}, {'$push': {'friends': username}})
    
    def removeFriend(self, username, friend):
        self.usersCollection.update_one({'username': username}, {'$pull': {'friends': friend}})
        self.usersCollection.update_one({'username': friend}, {'$pull': {'friends': username}})

    def updatePassword(self, username, password):
        self.usersCollection.update_one({'username': username}, {'$set': {'password': encryptPassword(password)}})
    
    def updateUsername(self, username, newUsername):
        self.usersCollection.update_one({'username': username}, {'$set': {'username': newUsername}})
    
    def close(self):
        self.client.close()

    def sendMsg(self, sender, receiver, msg, time):
        self.msgCollection.insert_one({'sender': sender, 'receiver': receiver, 'msg': msg, 'time': time, 'viewed': False})
    
    def getMsg(self, sender, receiver):
        batch1 = self.msgCollection.find({'sender': sender, 'receiver': receiver})
        batch2 = self.msgCollection.find({'sender': receiver, 'receiver': sender})
        messages = []
        for msg in batch1:
            messages.append(msg)
        for msg in batch2:
            messages.append(msg)
        # UPDATE ALL MESSAGES TO VIEWED
        #self.msgCollection.update_many({'sender': receiver, 'receiver': sender}, {'$set': {'viewed': True}})
        return json.loads(dumps(messages))

    def markAsRead(self, sender, receiver):
        self.msgCollection.update_many({'sender': receiver, 'receiver': sender}, {'$set': {'viewed': True}})
        
    # CHECK IF THERE IS NEW MESSAGE(S) AT ALL
    def checkMsgs(self, username):
        batch1 = self.msgCollection.find({'receiver': username, 'viewed': False})
        batch1 = json.loads(dumps(batch1))
        if len(batch1) > 0:
            # GET ALL USERS THAT SENT A MESSAGE
            users = []
            for msg in batch1:
                users.append(msg['sender'])
            # REMOVE DUPLICATES
            users = list(dict.fromkeys(users))
            return users
        return False

    def getUnreadMsg(self, start, end):
        messages = self.msgCollection.find({'sender': end, 'receiver': start, 'viewed': False})
        # UPDATE ALL MESSAGES TO VIEWED
        #self.msgCollection.update_many({'sender': end, 'receiver': start, 'viewed': False}, {'$set': {'viewed': True}})
        return json.loads(dumps(messages))
