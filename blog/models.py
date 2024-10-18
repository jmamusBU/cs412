from django.db import models

# Create your models here.

class Article(models.Model):
    '''Encapsulate the idea of one Article by some author.'''
    
    # data attributes of an Article
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateField(auto_now=True)
    #image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True) ## NEW
    
    def __str__(self):
        '''Return a string representation of this Article Object.'''
        return f'{self.title} by {self.author} on {self.published}'
    