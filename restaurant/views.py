from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random
import ast

spanish_omelette = ["Spanish Omelette", 15.99, ["Onion"]]
grilled_ribeye = ["Grilled Ribeye", 55.99, []]
paella = ["Paella", 25.99, ["Artichokes", "Mussels", "Shrimp"]]
chicken_teriyaki = ["Chicken Teriyaki", 15.99, ["Extra Sauce"]]
prime_porterhouse = ["Prime Porterhouse", 45.99, []]
unagi_nigiri = ["Unagi Nigiri", 7.99, ["Extra Ginger"]]


specials = [spanish_omelette, grilled_ribeye, paella]
regulars = [chicken_teriyaki, prime_porterhouse, unagi_nigiri]

# Create your views here.
def main(request):
    '''
    Function to handle the URL request for /restaurant (home page).
    Delegate rendering to the template restaurant/home.html.
    '''
    # use this template to render the response
    template_name = 'restaurant/main.html'

    # create a dictionary of context variables for the template:
    context = {
        "image" : "./myrestaurant.jpg",
    }

    # delegate rendering work to the template
    return render(request, template_name, context)

def order(request):
    '''
    Function to handle the URL request for /restaurant/order.
    Delegate rendering to the template restaurant/order.html.
    '''
    # use this template to render the response
    template_name = 'restaurant/order.html'

    # create a dictionary of context variables for the template:
    context = {
        "special" : random.choice(specials),
        "regulars" : regulars,
    }

    # delegate rendering work to the template
    return render(request, template_name, context)

def confirmation(request):
    '''
    Function to handle the URL request for /restaurant/confirmation.
    Delegate rendering to the template restaurant/confirmation.html.
    '''
    # use this template to render the response
    template_name = 'restaurant/confirmation.html'

    # create a dictionary of context variables for the template:
    results = []
    price = 0.0
    if request.POST:
        #print(request.POST)
        #print("************************")
        foods = request.POST.getlist("food")
        #print(foods)
        
        instructions = request.POST.get("instructions")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        
        #print(name)
        
        for i in range(len(foods)):
            #print("************************")
            f = ast.literal_eval(foods[i])
            #print(f)
            #print("////////////////////////")
            #print(f[0])
            results.append([f[0], f[1], []])
            price += f[1]
            
            if request.POST.getlist(f[0]):
                toppings = request.POST.getlist(f[0])
                #print(toppings)
                #print("*******************")
                for t in toppings:
                    results[i][2].append(t)
        
        #print(results)
        
        price = round(price, 2)
                    
        readytime = time.ctime(time.time() + random.randint(30,60)*60 - (4 * 60 * 60))
        #print(readytime)
            
    
    
        context = {
            "readytime" : readytime,
            "results" : results,
            "price" : price,
            "instructions" : instructions,
            "name" : name,
            "phone" : phone,
            "email" : email,
        }

    # delegate rendering work to the template
    return render(request, template_name, context=context)
