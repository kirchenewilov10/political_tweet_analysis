__author__ = 'com'

from django.urls import path
from . import views

urlpatterns = [
    path('register_twitter_task', views.register_twitter_task, name='register_twitter_task'),
]
