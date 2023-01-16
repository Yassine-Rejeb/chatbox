from django.shortcuts import render, HttpResponse
from django.urls import resolve
from django.shortcuts import redirect
from register.models import mongoConnection

def register(request):
    print('Register Page Opened!')
    report_loc = 'signup/'
    return render(request, 'register.html', {'loc':report_loc,'error': ''})


def signup(request):
    print('Register Request Made!')
    
    # GET REQUEST PARAMS
    email = request.POST['email']
    password = request.POST['password']
    password1 = request.POST['password1']
    username = request.POST['name']
    
    # VERIFY PASSWORDS MATCH
    dbConn = mongoConnection()
    if password != password1:
        return render(request, 'register.html', {'loc':'', 'error': 'Passwords do not match!'})
    
    # VERIFY EMAIL IS NOT TAKEN
    if dbConn.findEmail(email) != None:
        return render(request, 'register.html', {'loc':'', 'error': 'Email already exists!'})
    
    # VERIFY USERNAME IS NOT TAKEN
    if dbConn.findUsername(username) != None:
        return render(request, 'register.html', {'loc':'', 'error': 'Username already taken!'})
    
    # CREATE USER
    dbConn.insert(username, password, email, True)
    print('User Created!')

    # CLOSE DB CONNECTION
    dbConn.close()

    return redirect('/login/', {'loc':'', 'error': 'Account created! Please verify your email.'})

