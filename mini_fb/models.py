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
    
    def get_friends(self):
        '''Return a list of all friends for this Profile.'''
        friends_objects = Friend.objects.filter(profile1=self) | Friend.objects.filter(profile2=self)
        friends = []
        for f in friends_objects:
            if f.profile1 == self:
                friends.append(f.profile2)
            else:
                friends.append(f.profile1)
        return list(friends)
    
    def add_friend(self, other):
        '''adds a friend to this Profile.'''
        if self == other:
            raise ValueError("Self love.")
        if self in other.get_friends():
            raise ValueError("Duplicate friendship.")
        Friend.objects.create(profile1=self, profile2=other)
        
    def get_friend_suggestions(self):
        '''Return a list of friend suggestions for the Profile.'''
        friends = self.get_friends()
        suggestions = Profile.objects.exclude(pk=self.pk)
        for f in friends:
            suggestions = suggestions.exclude(pk=f.pk)
        return list(suggestions)
    
    
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
    
class Friend(models.Model):
    '''Stores a friendship between two Profiles.'''
    
    # data attributes of a Friend
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this Friend Object.'''
        return f'{self.profile1.first_name} {self.profile1.last_name} is homies with {self.profile2.first_name} {self.profile2.last_name}'
    