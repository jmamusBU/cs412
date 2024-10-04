# File: mini_fb/models.py
# Author: Jose Maria Amusategui Garcia Peri (jmamus@bu.edu) 04/10/2024
# Description: Defines the models for the mini_fb app

from django.db import models


class Profile(models.Model):
    '''Store Profile information for each user.'''
    
    # data attributes of an Article
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    image_url = models.URLField(blank=True)
    
    def __str__(self):
        '''Return a string representation of this Profile Object.'''
        return f'{self.first_name} {self.last_name} from {self.city}'
    