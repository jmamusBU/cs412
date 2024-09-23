## hw/views.py
## description: write view functions to handle URL requests for the hw app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.
# def home(request):
#     '''Handle the main URL for the hw app.'''

#     response_text = f'''
#     <html>
#     <h1>Hello, world!</h1>
#     <p>This is our first django web application!</p>
#     <hr>
#     This page was generated at {time.ctime()}.
#     </html>
#     '''
#     # create and return a response to the client:
#     return HttpResponse(response_text)

quotes = ["I don't know whether your heart ever necessarily changes, but time changes the way that you perceive the world. And you just hope it gives you more empathy and all those other things.",
          "Each song has its own secret that's different from another song, and each has its own life. Sometimes it has to be teased out, whereas other times it might come fast. There are no laws about songwriting or producing. It depends on what you're doing, not just who you're doing.",
          "I just want to be able to play and make people feel good with what I do. When you're thinking that way, anything can happen. And, usually, what happens is good.",
          "I just want to be able to play and make people feel good with what I do. When you're thinking that way, anything can happen. And, usually, what happens is good.",
          "I don't like definitions, but if there is a definition of freedom, it would be when you have control over your reality to transform it, to change it, rather than having it imposed upon you. You can't really ask for more than.",
          "Instead of receding, the past actually becomes more important. That's what will happen to you. It sounds unlikely, but the past actually changes complexion as you get older."]

images = ["https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Mar-Knopfler-Pensa-Blue.jpg/800px-Mar-Knopfler-Pensa-Blue.jpg",
          "data:image/jpeg;base64,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",
          "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRNUL3n988rohTK_-JkZuxGoOOb9iTCdWd8yw&s",
          "https://cdn.britannica.com/65/237665-050-1CD312AE/Mark-Knopfler-performs-London-2012.jpg",
          "https://cdn.britannica.com/64/237664-050-E80E8C19/Mark-Knopfler-Dire-Straits-1985-Live-Aid-London.jpg",
          "https://www.rollingstone.com/wp-content/uploads/2018/09/shutterstock_5280339bk.jpg",
          "https://www.irishtimes.com/resizer/v2/EQFNAYQB5BGHXFIG3GUDPBMVJI.jpg?auth=83aea05a280abde667ce452bec64a94db8ca7a57d2c47a7ac67eaa9619ec3630&smart=true&width=1024&height=1535"]

def home(request):
    '''
    Function to handle the URL request for /quotes (home page).
    Delegate rendering to the template quotes/home.html.
    '''
    # use this template to render the response
    template_name = 'quotes/quote.html'

    # create a dictionary of context variables for the template:
    context = {
        "current_time" : time.ctime(),
        "letter1" : chr(random.randint(65,90)), # a letter from A ... Z
        "letter2" : chr(random.randint(65,90)), # a letter from A ... Z
        "number" : random.randint(1,10), # number frmo 1 to 10
        "quote" : random.choice(quotes),
        "image" : random.choice(images),
    }

    # delegate rendering work to the template
    return render(request, template_name, context)


def about(request):
    '''
    Function to handle the URL request for /hw/about (about page).
    Delegate rendering to the template hw/about.html.
    '''
    # use this template to render the response
    template_name = 'quotes/about.html'

    # create a dictionary of context variables for the template:
    context = {
        "current_time" : time.ctime(),
    }

    # delegate rendering work to the template
    return render(request, template_name, context)

def show_all(request):
    
    # use this template to render the response
    template_name = 'quotes/show_all.html'

    # create a dictionary of context variables for the template:
    context = {
        "current_time" : time.ctime(),
        "quotes" : quotes,
        "images" : images,
    }
    # show all of the quotes and images

    # delegate rendering work to the template
    return render(request, template_name, context)

def quote(request):
        # use this template to render the response
        template_name = 'quotes/quote.html'
    
        # create a dictionary of context variables for the template:
        context = {
            "current_time" : time.ctime(),
            "quote" : random.choice(quotes),
            "image" : random.choice(images),
        }
    
        # delegate rendering work to the template
        return render(request, template_name, context)

def index(request):
    return HttpResponse("Hello, world. You're at the quotes index.")