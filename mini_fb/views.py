# File: mini_fb/models.py
# Author: Jose Maria Amusategui Garcia Peri (jmamus@bu.edu) 04/10/2024
# Description: Define the views for the mini_fb app
from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile
# Create your views here.

class ShowAllProfilesView(ListView):
    '''Generic view to display all profiles'''
    model = Profile # the model to display
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # context variable to use in the template
    