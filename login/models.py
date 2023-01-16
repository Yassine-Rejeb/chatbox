from django.db import models
import pymongo

def sendVerificationEmail(email):
    import smtplib, ssl
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "mohamedyassine.rejeb@gmail.com"  # Enter your address
    receiver_email = email  # Enter receiver address
    password = "mohamedyassine"
    message = ""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

class mongoConnection():
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://mongodb-server:27017/")
        self.db = self.client['chatbox']
        self.usersCollection = self.db['users']
    def insert(self, username, password, email, verified):
        self.usersCollection.insert_one({'username': username, 'password': password, 'email': email, 'verified': verified})
    def CheckCreds(self, username, password):
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
    def getEmail(self, username):
        return self.usersCollection.find({'username': username})['email']
    def close(self):
        self.client.close()
    