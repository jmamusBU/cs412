# File: project/forms.py
# Author: Jose Maria Amusategui Garcia Peri (jmamus@bu.edu) 8/12/2024
# Description: Defines the forms for the project app

from django import forms
from .models import *
        
    
class UpdateMusicForm(forms.ModelForm):
    '''Form to update a Music Object'''
    class Meta:
        model = Music
        fields = ['title', 'artistName', 'albumArtURL', 'genres']
        
class CreateMusicForm(forms.ModelForm):
    '''Form to create a Music Object.'''
    class Meta:
        model = Music
        fields = ['title', 'artistName', 'albumArtURL', 'genres']

        
