from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from .models import *
from django.db.models import Min, Max
import plotly
import plotly.graph_objects as go
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.urls import reverse

# Create your views here.
def testView(request):
    '''
    Function to handle the URL request for /restaurant (home page).
    Delegate rendering to the template restaurant/home.html.
    '''
    # use this template to render the response
    template_name = 'project/test.html'

    # create a dictionary of context variables for the template:
    context = {
        
    }

    # delegate rendering work to the template
    return render(request, template_name, context)

class OrderListView(LoginRequiredMixin, ListView):
    '''
    Class-based view to display a list of all orders.
    '''
    # specify the model for this view
    model = Order
    # specify the template to use for rendering
    template_name = 'project/orders.html'
    context_object_name = 'orders'
    paginate_by = 100
    
    def get_login_url(self):
        '''return the URL of the login page'''
        return reverse('login')
    
    def get_queryset(self):
        
        businessUser = BusinessUser.objects.get(user=self.request.user)
        qs = Order.objects.filter(locationId=businessUser.getLocationId())
        
        if 'consumer_name' in self.request.GET:
            name = self.request.GET['consumer_name']
            if name != '':
                qs = qs.filter(consumerName__icontains=name)
            
        if 'verification_code' in self.request.GET:
            code = self.request.GET['verification_code']
            if code != '':
                qs = qs.filter(verificationCode=code)
            
        if 'status' in self.request.GET:
            status = self.request.GET['status']
            if status != 'Any':
                qs = qs.filter(status=status)    
                
        if 'consumption' in self.request.GET:
            consumption = self.request.GET['consumption']
            if consumption != 'Any':
                qs = qs.filter(consumptionOrder=consumption)
                
        if 'min_date' in self.request.GET:
            min_date = self.request.GET['min_date']
            if min_date != '':
                qs = qs.filter(time__gte=min_date)
        
        if 'max_date' in self.request.GET:
            max_date = self.request.GET['max_date']
            if max_date != '':
                qs = qs.filter(time__lte=max_date)
        
        return qs.order_by('-time')
    
class OrderDetailView(LoginRequiredMixin, DetailView):
    '''Displays a detailed page for each order'''
    model = Order
    template_name = 'project/order_detail.html'
    context_object_name = 'o'

    def get_login_url(self):
        '''return the URL of the login page'''
        return reverse('login')
    
class DeleteOrderView(LoginRequiredMixin, DeleteView):
    '''Displays a page to delete a status message'''
    model = Order
    template_name = 'project/delete_order_form.html'
    context_object_name = 'o'
    
    def get_login_url(self):
        '''return the URL of the login page'''
        return reverse('login')
    
    def get_success_url(self):
        return reverse('orders')
    

class MusicListView(LoginRequiredMixin, ListView):
    '''
    Class-based view to display a list of all music.
    '''
    # specify the model for this view
    model = Music
    # specify the template to use for rendering
    template_name = 'project/music.html'
    context_object_name = 'music'
    paginate_by = 100
    
    def get_login_url(self):
        '''return the URL of the login page'''
        return reverse('login')
    
    def get_queryset(self):

        businessUser = BusinessUser.objects.get(user=self.request.user)
        qs = Music.objects.filter(locationId=businessUser.getLocationId().id)
        
        if 'artist' in self.request.GET:
            artist = self.request.GET['artist']
            if artist != '':
                qs = qs.filter(artistName__icontains=artist)
            
        if 'title' in self.request.GET:
            title = self.request.GET['title']
            if title != '':
                qs = qs.filter(title__icontains=title)
                
                
        if 'min_date' in self.request.GET:
            min_date = self.request.GET['min_date']
            if min_date != '':
                qs = qs.filter(timestamp__gte=min_date)
        
        if 'max_date' in self.request.GET:
            max_date = self.request.GET['max_date']
            if max_date != '':
                qs = qs.filter(timestamp__lte=max_date)
        
        return qs.order_by('-timestamp')
    