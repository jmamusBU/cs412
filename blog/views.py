# blog/views.py
# define the views for the blog app
from django.shortcuts import render
from django.views.generic import ListView
from .models import *
# Create your views here.

class ShowAllView(ListView):
    model = Article # the model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # context variable to use in the template
    