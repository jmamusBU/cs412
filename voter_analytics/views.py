from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Min, Max
from typing import Any
import plotly
import plotly.graph_objects as go

# Create your views here.

class VoterListView(ListView):
    '''Displays a list of all voters'''
    model = Voter
    template_name = 'voter_analytics/results.html'
    context_object_name = 'voters'
    paginate_by = 100
    
    def get_context_data(self, **kwargs: Any):
        '''Adds context for search filters'''
        context = super().get_context_data(**kwargs)
        
        min_dob = Voter.objects.aggregate(Min('dob'))
        min_dob_year = min_dob.get('dob__min').year
        max_dob = Voter.objects.aggregate(Max('dob'))
        max_dob_year = max_dob.get('dob__max').year
        dob_list = []
        for i in range(min_dob_year, max_dob_year+1):
            dob_list.append(i)
        context['dob_list'] = dob_list
        return context
    
    def get_queryset(self):
        '''Filters records shown depending on user input'''
        qs = super().get_queryset()
        
        qs = Voter.objects.all()
        
        
        if 'party' in self.request.GET:
            party = self.request.GET['party']
            if party != 'Any':
                qs = qs.filter(party__icontains=party)
            
            
        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            if min_dob != 'Any':
                qs = qs.filter(dob__year__gte=min_dob)
            
        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob != 'Any':
                qs = qs.filter(dob__year__lte=max_dob)
                
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score != 'Any':
                qs = qs.filter(voter_score=voter_score)
                
        if 'v20state' in self.request.GET:
            qs = qs.filter(state=True)
            
        if 'v21town' in self.request.GET:
            qs = qs.filter(v21town=True)
            
        if 'v21primary' in self.request.GET:
            qs = qs.filter(primary=True)
            
        if 'v22general' in self.request.GET:
            qs = qs.filter(general=True)
            
        if 'v23town' in self.request.GET:
            qs = qs.filter(v23town=True)
        
        return qs.order_by('last_name', 'first_name')
        
def search(request):
    '''Displays search form, for testing'''
    template_name = 'voter_analytics/search.html'
    min_dob = Voter.objects.aggregate(Min('dob'))
    min_dob_year = min_dob.get('dob__min').year
    max_dob = Voter.objects.aggregate(Max('dob'))
    max_dob_year = max_dob.get('dob__max').year
    dob_list = []
    
    for i in range(min_dob_year, max_dob_year+1):
        dob_list.append(i)
    context = {
        "dob_list": dob_list,
    }
    print(dob_list)
    return render(request, template_name, context) 

class VoterView(DetailView):
    '''Displays a detailed page for each voter'''
    model = Voter
    template_name = 'voter_analytics/voter.html'
    context_object_name = 'v'
    
class GraphView(ListView):
    '''Displays several graphs to show voter data'''
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'
    
    def get_queryset(self):
        '''Filters records shown depending on user input'''
        qs = super().get_queryset()
        
        qs = Voter.objects.all()
        
        
        if 'party' in self.request.GET:
            party = self.request.GET['party']
            if party != 'Any':
                qs = qs.filter(party__icontains=party)
            
            
        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            if min_dob != 'Any':
                qs = qs.filter(dob__year__gte=min_dob)
            
        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob != 'Any':
                qs = qs.filter(dob__year__lte=max_dob)
                
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score != 'Any':
                qs = qs.filter(voter_score=voter_score)
                
        if 'v20state' in self.request.GET:
            qs = qs.filter(state=True)
            
        if 'v21town' in self.request.GET:
            qs = qs.filter(v21town=True)
            
        if 'v21primary' in self.request.GET:
            qs = qs.filter(primary=True)
            
        if 'v22general' in self.request.GET:
            qs = qs.filter(general=True)
            
        if 'v23town' in self.request.GET:
            qs = qs.filter(v23town=True)
        
        return qs.order_by('last_name', 'first_name')
    
    def get_context_data(self, **kwargs: Any):
        '''Adds context for search filters'''
        context = super().get_context_data(**kwargs)
        
        qs = self.get_queryset()
        
        min_dob = Voter.objects.aggregate(Min('dob'))
        min_dob_year = min_dob.get('dob__min').year
        max_dob = Voter.objects.aggregate(Max('dob'))
        max_dob_year = max_dob.get('dob__max').year
        og_dob_list = []
    
        for i in range(min_dob_year, max_dob_year+1):
            og_dob_list.append(i)
        context['og_dob_list'] = og_dob_list
        
        min_dob = qs.aggregate(Min('dob'))
        min_dob_year = min_dob.get('dob__min').year
        max_dob = qs.aggregate(Max('dob'))
        max_dob_year = max_dob.get('dob__max').year
        dob_list = []
        for i in range(min_dob_year, max_dob_year+1):
            dob_list.append(i)
        barx = dob_list
        bary = []
        
        for d in dob_list:
            bary.append(qs.filter(dob__year=d).count())
            
        bar = go.Bar(x=barx, y=bary)
        bar_div = plotly.offline.plot({'data':[bar]}, auto_open=False, output_type='div')
        
        context['bar_div'] = bar_div
        
        piex = ["U", "D", "R", "CC", "L", "T", "O", "G", "J", "Q", "FF"]
        piey = []
        
        for x in piex:
            piey.append(qs.filter(party=x).count())
            
        fig = go.Pie(labels=piex, values=piey)
        pie_div = plotly.offline.plot({'data':[fig]}, auto_open=False, output_type='div')
        
        context['pie_div'] = pie_div
        
        histx = ["v20state", "v21town", "v21primary", "v22general", "v23town"]
        histy = []
        
        for x in histx:
            if x == "v20state":
                histy.append(qs.filter(state=True).count())
            elif x == "v21town":
                histy.append(qs.filter(v21town=True).count())
            elif x == "v21primary":
                histy.append(qs.filter(primary=True).count())
            elif x == "v22general":
                histy.append(qs.filter(general=True).count())
            elif x == "v23town":
                histy.append(qs.filter(v23town=True).count())

        bar = go.Bar(x=histx, y=histy)
        hist_div = plotly.offline.plot({'data':[bar]}, auto_open=False, output_type='div')
        
        context['hist_div'] = hist_div
        return context
    
    
    
