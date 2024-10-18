# File: mini_fb/forms.py
# Author: Jose Maria Amusategui Garcia Peri (jmamus@bu.edu) 09/10/2024
# Description: Defines the forms for the mini_fb app

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''Form to create a Profile.'''
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'image_url']
        
class CreateStatusMessageForm(forms.ModelForm):
    '''Form to create a Status Message'''
    class Meta:
        model = StatusMessage
        fields = ['message']
        
    
class UpdateProfileForm(forms.ModelForm):
    '''Form to update a Profile.'''
    class Meta:
        model = Profile
        fields = ['city', 'email_address', 'image_url']
        
class UpdateStatusMessageForm(forms.ModelForm):
    '''Form to update a Status Message'''
    class Meta:
        model = StatusMessage
        fields = ['message']