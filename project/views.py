from django.shortcuts import render

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