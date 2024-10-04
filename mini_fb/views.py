# mini_fb/views.py
# define the views for the blog app
from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile
# Create your views here.

class ShowAllView(ListView):
    model = Profile # the model to display
    template_name = 'mini_fb/show_all.html'
    context_object_name = 'profiles' # context variable to use in the template
    