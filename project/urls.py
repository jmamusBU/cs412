# File: mini_fb/urls.py
# Author: Jose Maria Amusategui Garcia Peri (jmamus@bu.edu) 04/10/2024
# Description: URL patterns for the mini_fb app

from django.urls import path
from django.conf import settings
from .views import *
from django.contrib.auth import views as auth_views

from . import views
#User Credentials:
#Username: magerit
#Password: LMBB2023

# all of the URLs that are part of this app
urlpatterns = [
    path(r'', views.testView, name='test_view'),
    path(r'orders/', OrderListView.as_view(), name='orders'),
    path(r'music/', MusicListView.as_view(), name='music'),
    path(r'login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path(r'logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),
    path(r'order_detail/<str:pk>', views.OrderDetailView.as_view(), name='orderDetail'),
    path(r'order_detail/<str:pk>/delete', DeleteOrderView.as_view(), name="delete_order"),
]