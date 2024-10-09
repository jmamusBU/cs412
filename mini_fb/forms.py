from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''Form to create a Profile.'''
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'image_url']
        
    