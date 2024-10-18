# File: mini_fb/urls.py
# Author: Jose Maria Amusategui Garcia Peri (jmamus@bu.edu) 04/10/2024
# Description: URL patterns for the mini_fb app

from django.urls import path
from django.conf import settings
from .views import *

# all of the URLs that are part of this app
urlpatterns = [
    path(r'', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path(r'profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"),
    path(r'create_profile', CreateProfileView.as_view(), name="create_profile"),
    path(r'profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name="create_status"),   
    path(r'profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
]