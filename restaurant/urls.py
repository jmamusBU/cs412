## hw/urls.py
## description: URL patterns for the hw app

from django.urls import path
from django.conf import settings
from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path("", views.main, name="main"),
    path("main", views.main, name="main"),
    path("order", views.order, name="order"),
    path("confirmation", views.confirmation, name="confirmation"),
    
]