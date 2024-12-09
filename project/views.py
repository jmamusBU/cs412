from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, TemplateView
from .models import *
from django.db.models import Min, Max
import plotly
import plotly.graph_objects as go
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.urls import reverse
from .forms import *
import uuid
import plotly
import plotly.graph_objects as go
import datetime

# Create your views here.

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
    '''Displays a page to delete an order'''
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

class MusicDetailView(LoginRequiredMixin, DetailView):
    '''Displays a detailed page for each song'''
    model = Music
    template_name = 'project/music_detail.html'
    context_object_name = 'm'

    def get_login_url(self):
        '''return the URL of the login page'''
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        '''Adds the genres to the context data'''
        context = super().get_context_data(**kwargs)
        genres = Music.objects.get(id=self.kwargs['pk']).genres
        context['genres'] = json.loads(genres)
        print(json.loads(genres)) 
        return context
    
class DeleteMusicView(LoginRequiredMixin, DeleteView):
    '''Displays a page to delete a status message'''
    model = Music
    template_name = 'project/delete_music_form.html'
    context_object_name = 'm'
    
    def get_login_url(self):
        '''return the URL of the login page'''
        return reverse('login')
    
    def get_success_url(self):
        return reverse('music')
    
    def get_context_data(self, **kwargs):
        '''Adds the profile to the context data so that the form can be submitted'''
        context = super().get_context_data(**kwargs)
        genres = Music.objects.get(id=self.kwargs['pk']).genres
        context['genres'] = json.loads(genres)
        print(json.loads(genres)) 
        return context
    
class UpdateMusicView(LoginRequiredMixin, UpdateView):
    '''Displays a page to update a Music Object'''
    form_class = UpdateMusicForm
    template_name = 'project/update_music_form.html'
    model = Music
    
    def get_login_url(self):
        '''return the URL of the login page'''
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        '''Adds the music to the context data so that the form can be submitted'''
        context = super().get_context_data(**kwargs)
        genres = Music.objects.get(id=self.kwargs['pk']).genres
        context['genres'] = json.loads(genres)
        music = Music.objects.get(id=self.kwargs['pk'])
        context['m'] = music
        print(json.loads(genres)) 
        return context
    
    def get_success_url(self):
        return reverse('music')
    
class CreateMusicView(LoginRequiredMixin, CreateView):
    '''Displays a page to create a Music Object'''
    form_class = CreateMusicForm
    template_name = 'project/create_music_form.html' 
    
    
    def get_login_url(self):
        '''return the URL of the login page'''
        return reverse('login')
    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        businessUser = BusinessUser.objects.get(user=self.request.user)
        locationId = businessUser.getLocationId().id
        context['locationId'] = locationId 
        return context
    '''
    
    def form_valid(self, form):
        businessUser = BusinessUser.objects.get(user=self.request.user)
        locationId = businessUser.getLocationId().id
        form.instance.timestamp = datetime.datetime.now()
        form.instance.locationId = locationId
        form.instance.id = str(uuid.uuid4())
        # save the music object to database
        form.save()
            
        return super().form_valid(form)
    

class GraphView(LoginRequiredMixin, TemplateView):
    '''Displays several graphs to show order and music data'''
    
    # Using TemplateView instead of ListView because we are displaying multiple graphs
    # for two different models, Order and Music
    
    template_name = 'project/graphs.html'
    
    def get_login_url(self):
        '''return the URL of the login page'''
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        '''Adds the data for the graphs to the context data'''
        # need to create and add two different query sets to the context data 
        # for the two different models
        
        context = super().get_context_data(**kwargs)
        businessUser = BusinessUser.objects.get(user=self.request.user)
        
        orders_qs = Order.objects.filter(locationId=businessUser.getLocationId())
        
        if 'consumer_name' in self.request.GET:
            name = self.request.GET['consumer_name']
            if name != '':
                orders_qs = orders_qs.filter(consumerName__icontains=name)
            
        if 'verification_code' in self.request.GET:
            code = self.request.GET['verification_code']
            if code != '':
                orders_qs = orders_qs.filter(verificationCode=code)
            
        if 'status' in self.request.GET:
            status = self.request.GET['status']
            if status != 'Any':
                orders_qs = orders_qs.filter(status=status)    
                
        if 'consumption' in self.request.GET:
            consumption = self.request.GET['consumption']
            if consumption != 'Any':
                orders_qs = orders_qs.filter(consumptionOrder=consumption)
                
        if 'min_date' in self.request.GET:
            min_date = self.request.GET['min_date']
            if min_date != '':
                orders_qs = orders_qs.filter(time__gte=min_date)
        
        if 'max_date' in self.request.GET:
            max_date = self.request.GET['max_date']
            if max_date != '':
                orders_qs = orders_qs.filter(time__lte=max_date)
                
        context['orders'] = orders_qs.order_by('-time')
        
        music_qs = Music.objects.filter(locationId=businessUser.getLocationId().id)
        
        if 'artist' in self.request.GET:
            artist = self.request.GET['artist']
            if artist != '':
                music_qs = music_qs.filter(artistName__icontains=artist)
            
        if 'title' in self.request.GET:
            title = self.request.GET['title']
            if title != '':
                music_qs = music_qs.filter(title__icontains=title)
                
                
        if 'min_date' in self.request.GET:
            min_date = self.request.GET['min_date']
            if min_date != '':
                music_qs = music_qs.filter(timestamp__gte=min_date)
        
        if 'max_date' in self.request.GET:
            max_date = self.request.GET['max_date']
            if max_date != '':
                music_qs = music_qs.filter(timestamp__lte=max_date)
                
        context['music'] = music_qs.order_by('-timestamp')
        
        # pie chart for orders by status
        piex = ["PICKUP", "DONE", "IN_QUEUE"]
        piey = []
        
        for x in piex:
            piey.append(orders_qs.filter(status=x).count())
            
            
        fig = go.Pie(labels=piex, values=piey)
        pie_div = plotly.offline.plot({'data':[fig]}, auto_open=False, output_type='div')
            
        context['pie_div'] = pie_div
        
        # bar chart for number of orders per day
        barx = []
        bary = []
        for o in orders_qs:
            #days from min_date to max_date
            if o.time.date() not in barx:
                barx.append(o.time.date())
        
        for x in barx:
            bary.append(orders_qs.filter(time__date=x).count())
        
        bar = go.Bar(x=barx, y=bary)   
        bar_div = plotly.offline.plot({'data':[bar]}, auto_open=False, output_type='div')
        
        context['bar_div'] = bar_div
        
        #Scatter plot for orders by time and amount paid
        
        orders_scatterx = []
        orders_scattery = []
        orders_names = []
        
        for o in orders_qs:
            orders_scatterx.append(o.time)
            orders_scattery.append(o.amountPaidCents)
            #add drinks to names
            result = ""
            for d in o.drinkOrderCounts.all():
                
                if d.drinkOrder.drinkId:
                    result += d.drinkOrder.drinkId.name
                if d.drinkOrder.mixerId:
                    result += d.drinkOrder.mixerId.name
                result += " x" + str(d.count) + " "
                
                print(d.drinkOrder.drinkId.name)
            orders_names.append(result)
                
                
        
        orders_scatter = go.Scatter(x=orders_scatterx, y=orders_scattery, mode='markers', text=orders_names)
        orders_scatter_div = plotly.offline.plot({'data':[orders_scatter]}, auto_open=False, output_type='div')
        
        context['orders_scatter_div'] = orders_scatter_div
        
        
        # pie chart for music by time
        music_scatterx = []
        music_scattery = []
        music_names = []
        
        for m in music_qs:
            music_scatterx.append(m.timestamp)
            # 1 for each song
            music_scattery.append(1)
            
            music_names.append(m.title + " by " + m.artistName + " at " + str(m.timestamp.time()))
            
    
   
        music_scatter = go.Scatter(x=music_scatterx, y=music_scattery, mode='markers', text=music_names)
        music_scatter_div = plotly.offline.plot({'data':[music_scatter]}, auto_open=False, output_type='div')
        
        context['music_scatter_div'] = music_scatter_div
        
        
        return context
        