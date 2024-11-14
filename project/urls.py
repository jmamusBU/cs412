# File: mini_fb/urls.py
# Author: Jose Maria Amusategui Garcia Peri (jmamus@bu.edu) 04/10/2024
# Description: URL patterns for the mini_fb app

from django.urls import path
from django.conf import settings
from .views import *
from django.contrib.auth import views as auth_views

from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path(r'', views.testView, name='test_view'),
]