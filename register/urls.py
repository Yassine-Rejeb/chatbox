from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('signup/', views.signup, name='register'),
]