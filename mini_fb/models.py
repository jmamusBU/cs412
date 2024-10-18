# File: mini_fb/models.py
# Author: Jose Maria Amusategui Garcia Peri (jmamus@bu.edu) 04/10/2024
# Description: Defines the models for the mini_fb app

from django.db import models
from django.urls import reverse


class Profile(models.Model):
    '''Store Profile information for each user.'''
    
    # data attributes of a Profile
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    image_url = models.URLField(blank=True)
    
    def __str__(self):
        '''Return a string representation of this Profile Object.'''
        return f'{self.first_name} {self.last_name} from {self.city}'
    
    def get_status_messages(self):
        '''Return a QuerySet of all status messages for this Profile.'''
        messages = StatusMessage.objects.filter(profile=self)
        return messages
    
    def get_absolute_url(self):
        return reverse("show_profile", kwargs={"pk": self.pk})
    
    
class StatusMessage(models.Model):
    '''Store a status message for each Profile.'''
    
    # data attributes of a StatusMessage
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this StatusMessage Object.'''
        return f'{self.profile.first_name} {self.profile.last_name} said {self.message} at {self.created_at}'
    
    def get_absolute_url(self):
        return reverse("show_profile", kwargs={"pk": self.profile.pk})
    
    def get_images(self):
        '''Return a QuerySet of all images for this StatusMessage.'''
        images = Image.objects.filter(status_message=self)
        return images
    
class Image(models.Model):
    '''Stores an image for a StatusMessage'''
    
    # data attributes of an Image
    image_file = models.ImageField(blank=True)
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    
    