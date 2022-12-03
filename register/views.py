from django.shortcuts import render, HttpResponse
from django.urls import resolve
from django.shortcuts import redirect
from register.models import mongoConnection

times = 0
def register(request):
    global times
    print('Register Page Opened!')
    times += 1
    current_url = request.path
    print(current_url)
    print(0)
    if request.path == '/register/signup/':
        report_loc = '../signup/'
    else: report_loc = 'signup/'
    return render(request, 'register.html', {'loc':report_loc,'error': ''})
def signup(request):
    print('Register Request Made!')
    dbConn = mongoConnection()
    email = request.POST['email']
    password = request.POST['password']
    password1 = request.POST['password1']
    username = request.POST['name']
    print("Email: " + email)
    print("Username: " + username)
    print("Password: " + password)
    print("Password1: " + password1)
    if password != password1:
        return render(request, 'register.html', {'loc':'..', 'error': 'Passwords do not match!'})
    if dbConn.findEmail(email) != None:
        return render(request, 'register.html', {'loc':'..', 'error': 'Email already exists!'})
    if dbConn.findUsername(username) != None:
        return render(request, 'register.html', {'loc':'..', 'error': 'Username already taken!'})
    dbConn.insert(username, password, email, False)
    render(request, 'register.html', {'loc':'..', 'error': 'Account created! Please verify your email.'})
    return redirect('/login/', {'loc':'..', 'error': 'Account created! Please verify your email.'})
