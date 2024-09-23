## hw/urls.py
## description: URL patterns for the hw app

from django.urls import path
from django.conf import settings
from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path(r'', views.home, name="home"),
    path(r'about', views.about, name="about"),
    path("", views.index, name="index"),
    path("show_all", views.show_all, name="show_all"),
    path("quote", views.quote, name="quote"),
    
]