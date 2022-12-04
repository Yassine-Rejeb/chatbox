from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from chat import models

# Create your views here.

def index(response):
    return HttpResponse("<h1>Hi, this is a python+crypto project!</h1>")

def unknown(response):
    print('Not a known user!')
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

def chat(response):
    # CHECK IF USER IS LOGGED IN
    if unknown(response):
        return redirect('/login/')
    print('Chat Page Opened!')
    
    # GET USERNAME
    print("Session USER:",response.session['username'])
    return render(response, "chat/chat.html",  {'current_user': response.session['username']})