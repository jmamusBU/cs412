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
    path(r'', views.VoterListView.as_view(), name='voters'),
    path(r'search', views.search, name='search'),
    path(r'voter/<int:pk>', views.VoterView.as_view(), name='voter'),
    path(r'graphs', views.GraphView.as_view(), name='graphs'),
]