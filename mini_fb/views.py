# File: mini_fb/models.py
# Author: Jose Maria Amusategui Garcia Peri (jmamus@bu.edu) 04/10/2024
# Description: Define the views for the mini_fb app
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import CreateProfileForm, CreateStatusMessageForm
# Create your views here.

class ShowAllProfilesView(ListView):
    '''Generic view to display all profiles'''
    model = Profile # the model to display
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # context variable to use in the template
    
class ShowProfilePageView(DetailView):
    '''Displays a single profile page, selected by PK'''
    model = Profile # the model to display
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile' # context variable to use in the template
    
class CreateProfileView(CreateView):
    '''Displays a page to create a profile'''
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html' 
    
class CreateStatusMessageView(CreateView):
    '''Displays a page to create a status message'''
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile 
        return context
    
    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        return super().form_valid(form)
    
    
    
    