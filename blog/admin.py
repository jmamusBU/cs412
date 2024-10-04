from django.contrib import admin

# Register your models here.

# tell the admin we want to administer these models
from .models import Article
admin.site.register(Article)