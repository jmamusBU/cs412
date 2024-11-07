# File: voter_analytics/urls.py
# Author: Jose Maria Amusategui Garcia Peri (jmamus@bu.edu) 07/11/2024
# Description: URL patterns for the voter_analytics app

from django.urls import path
from django.conf import settings
from .views import *
from django.contrib.auth import views as auth_views

from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path(r'', views.BallsView, name='show_all_profiles'),

]