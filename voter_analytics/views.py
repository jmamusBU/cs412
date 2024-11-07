from django.shortcuts import render

# Create your views here.

def BallsView(request):
    template_name = 'voter_analytics/balls.html'
    context = {
        "balls": "balls",
    }
    
    return render(request, template_name, context)