from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(response):
    return HttpResponse("<h1>Hi, this is a python+crypto project!</h1>")

def chat(response):
    return render(response, "chat/chat.html",  {})