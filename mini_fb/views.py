# File: mini_fb/models.py
# Author: Jose Maria Amusategui Garcia Peri (jmamus@bu.edu) 04/10/2024
# Description: Define the views for the mini_fb app

from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from typing import Any
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View 
from .models import * ## import the models (e.g., Article)
from .forms import * ## import the forms (e.g., CreateCommentForm)
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login ## NEW
import random

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
    
    def get_login_url(self):
        '''return the URL of the login page'''
        return reverse('login')
    
    def form_valid(self, form):
        '''This method is called as port of the form processing'''
        
        print(f'CreateProfileView.form_valid(): form.cleaned_data={form.cleaned_data}')
        
        user = self.request.user
        
        form.instance.user = user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        user_form = UserCreationForm()
        context['user_form'] = user_form
        return context
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        '''Handle the user creation form submission'''
        
        if self.request.POST:
            print(f"CreateProfileView.dispatch: self.request.POST={self.request.POST}")
            
            user_form = UserCreationForm(self.request.POST)
            
            if not user_form.is_valid():
                print(f"form.errors={form.errors}")

                return super().dispatch(request, *args, **kwargs)
            
            user = user_form.save()
            
            
            print(f"user={user}")
            
            login(self.request, user)
            print(f"User {user} logged in.")
            
        
        return super().dispatch(request, *args, **kwargs)
        
    
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''Displays a page to create a status message'''
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html' 
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
    def get_login_url(self):
        '''return the URL of the login page'''
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        '''Adds the profile to the context data so that the form can be submitted'''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile 
        return context
    
    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.profile = profile
        # save the status message to database
        sm = form.save()
        # read the file from the form:
        files = self.request.FILES.getlist('files')
        
        for f in files:
            image = Image(status_message=sm, image_file=f)
            image.save()
            
        return super().form_valid(form)
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''Displays a page to update a profile'''
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    model = Profile
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
    def get_login_url(self):
        '''return the URL of the login page'''
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        '''Adds the profile to the context data so that the form can be submitted'''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile 
        return context
    
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''Displays a page to delete a status message'''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'
    
    def get_login_url(self):
        '''return the URL of the login page'''
        return reverse('login')
    
    def get_success_url(self):
        pk = self.kwargs.get('pk')
        status_message = StatusMessage.objects.filter(pk=pk).first()
        profile = status_message.profile
        return reverse('show_profile', kwargs={'pk': profile.pk})
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''Displays a page to update a status message'''
    form_class = UpdateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    model = StatusMessage
    context_object_name = 'status_message'
    
    def get_login_url(self):
        '''return the URL of the login page'''
        return reverse('login')
    
    def get_success_url(self):
        pk = self.kwargs.get('pk')
        status_message = StatusMessage.objects.filter(pk=pk).first()
        profile = status_message.profile
        return reverse('show_profile', kwargs={'pk': profile.pk})
    
class CreateFriendView(LoginRequiredMixin, View):
    '''processes a request to add a friend to a profile'''
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
    def get_login_url(self):
        '''return the URL of the login page'''
        return reverse('login')
    
    def dispatch(self, request, *args, **kwargs):
        pk1 = self.kwargs.get('pk')
        pk2 = self.kwargs.get('other_pk')
        profile1 = Profile.objects.get(user=self.request.user)
        profile2 = Profile.objects.get(pk=pk2)
        profile1.add_friend(profile2)
        return redirect(profile1.get_absolute_url())
    
    
    
class ShowFriendSuggestionsView(DetailView):
    '''Displays a page to show friend suggestions for a given profile'''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
class ShowNewsFeedView(DetailView):
    '''Displays a page to show the news feed for a given profile'''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    