from django.db import models

# Create your models here.

class Profile(models.Model):
    '''Store Profile information for each user.'''
    
    # data attributes of an Article
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    image_url = models.URLField(blank=True)
    
    def __str__(self):
        '''Return a string representation of this Article Object.'''
        return f'{self.first_name} {self.last_name} from {self.city}'
    