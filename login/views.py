from django.shortcuts import render
import json
from chat import views
from login.models import mongoConnection
from django.shortcuts import redirect

def alreadyLoggedIn(request):
    #print('Already Logged In!')
    if 'username' in request.session:
        return True
    return False

def login(request):
    # CHECK IF USER IS LOGGED IN
    if alreadyLoggedIn(request):
        return redirect('/chat/')

    #print('Login Page Opened!')

    report_loc = 'signin/'
    return render(request, 'login.html', {'loc':report_loc,'error': ''})

def encryptPassword(password):
    # Hash a password with SHA256
    import hashlib
    hash_object = hashlib.sha256(password.encode())
    return hash_object.hexdigest()

def signin(request):
    # CHECK IF USER IS LOGGED IN
    if alreadyLoggedIn(request):
        return redirect('/chat/')
    
    #print('Login Request Made!')
    
    # GET REQUEST PARAMS
    email = request.POST['email']
    password = request.POST['password']

    # CHECK IF USER EXISTS
    dbConn = mongoConnection()
    if dbConn.findEmail(email) == None:
        return render(request, 'login.html', {'loc':'','error': 'Email and password do not match!'})

    # CHECK IF EMAIL IS VERIFIED
    if dbConn.findEmailWhenVerified(email) == None:
        print('Email not found!')
        return render(request, 'login.html', {'loc':'','error': 'Email not verified!'})
    
    # CHECK IF PASSWORD IS CORRECT
    user=dbConn.findEmail(email)
    if  user['password'] != encryptPassword(password):
        print('Password incorrect!')
        # CLOSE DB CONNECTION
        dbConn.close()
        return render(request, 'login.html', {'loc':'','error': 'Email and password do not match!'})
    else:
        print('Login Successful!')
        print(user['username'])
        request.session['username'] = user['username']
        # CLOSE DB CONNECTION
        dbConn.close()
        return redirect('/chat/')
    