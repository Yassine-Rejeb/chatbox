from django.urls import path, include
from django.contrib import auth
from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path("", views.chat, name="chat room"),
]