import json
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from chat import models

# Create your views here.

def index(response):
    return HttpResponse("<h1>Hi, this is a python+crypto project!</h1>")

def unknown(response):
    if 'username' not in response.session:
        return True
    return False

def Logout(response):
    # CHECK IF USER IS LOGGED IN
    if unknown(response):
        return redirect('/login/')

    # LOGOUT USER
    del response.session['username']
    return redirect('/login/')

def getFriends(response):
    # CHECK IF USER IS LOGGED IN
    if unknown(response):
        return redirect('/login/')
    print('Friends Page Opened!')
    dbConn = models.mongoConnection()
    friends = dbConn.findFriends(response.session['username'])
    print("RESULT:",json.dumps(friends))
    # GET USERNAME
    print("Session USER:",response.session['username'])
    return jsonresponse(json.dumps(friends))

def chat(response):
    # CHECK IF USER IS LOGGED IN
    if unknown(response):
        return redirect('/login/')
    print('Chat Page Opened!')
    
    # GET USERNAME
    print("Session USER:",response.session['username'])
    return render(response, "chat/chat.html",  {'current_user': response.session['username']})