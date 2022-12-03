from django.shortcuts import render, HttpResponse
import json
from chat import views
from login.models import mongoConnection
from django.shortcuts import redirect

times = 0
def login(request):
    global times
    print('Login Page Opened!')
    times += 1
    if request.path == '/login/signin/':
        report_loc = '../signin/'
    else: report_loc = 'signin/'
    return render(request, 'login.html', {'loc':report_loc,'error': ''})
def signin(request):
    print('Login Request Made!')
    dbConn = mongoConnection()
    email = request.POST['email']
    password = request.POST['password']
    print("Email: " + email)
    print("Password: " + password)
    if dbConn.find(email, password) == None:
        return render(request, 'login.html', {'loc':'..', 'error': 'Invalid email/password!'})
    elif dbConn.findEmailWhenVerified(email) == None:
        return render(request, 'login.html', {'loc':'..', 'error': 'Email not verified!'})
    else:
        return redirect(views.chat, {'loc':'..', 'error': 'Login successful!'})
    
    