# File: mini_fb/models.py
# Author: Jose Maria Amusategui Garcia Peri (jmamus@bu.edu) 04/10/2024
# Description: Define the views for the mini_fb app
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
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
        '''Adds the profile to the context data so that the form can be submitted'''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile 
        return context
    
    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        # save the status message to database
        sm = form.save()
        # read the file from the form:
        files = self.request.FILES.getlist('files')
        
        for f in files:
            image = Image(status_message=sm, image_file=f)
            image.save()
            
        return super().form_valid(form)
    
class UpdateProfileView(UpdateView):
    '''Displays a page to update a profile'''
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    model = Profile
    
    def get_context_data(self, **kwargs):
        '''Adds the profile to the context data so that the form can be submitted'''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile 
        return context
    
class DeleteStatusMessageView(DeleteView):
    '''Displays a page to delete a status message'''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'
    
    def get_success_url(self):
        pk = self.kwargs.get('pk')
        status_message = StatusMessage.objects.filter(pk=pk).first()
        profile = status_message.profile
        return reverse('show_profile', kwargs={'pk': profile.pk})
    
class UpdateStatusMessageView(UpdateView):
    '''Displays a page to update a status message'''
    form_class = UpdateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    model = StatusMessage
    context_object_name = 'status_message'
    
    def get_success_url(self):
        pk = self.kwargs.get('pk')
        status_message = StatusMessage.objects.filter(pk=pk).first()
        profile = status_message.profile
        return reverse('show_profile', kwargs={'pk': profile.pk})