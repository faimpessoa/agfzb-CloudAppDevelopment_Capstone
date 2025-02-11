from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import requests

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def get_about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def get_contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contacts.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)



# Update the `get_dealerships` view to render the index page with a list of dealerships
#def get_dealerships(request):
#    context = {}
#    if request.method == "GET":
#        external_api_url = "https://faimpessoa-3000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get" 
#                           # https://faimpessoa-3000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get
#        dealershipsdata = requests.get(external_api_url)
#        print("called")
#        data = json.loads(dealershipsdata.text)
#        context['dealerships'] = data
#        return render(request, 'djangoapp/index.html', context)
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://faimpessoa-3000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context['dealerships'] = dealerships
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)
       



# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://faimpessoa-3000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        for dealer in dealerships:
            if dealer.id == dealer_id:
                context['dealerName'] = dealer.full_name
                context['dealerShortName'] = dealer.short_name
        
        url = "https://faimpessoa-5000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        # Get dealers from the URL
        dealership_reviews = get_dealer_reviews_from_cf(url, id=dealer_id)
        context['reviews'] = dealership_reviews
        context['dealerID'] = dealer_id
        
        # Concat all dealer's short name
        #review_texts = ' '.join([rev.review for rev in dealership_reviews])
        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    result = "Not Authenticated"
    context = {}
    if request.method == "GET":
        url = "https://faimpessoa-3000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        for dealer in dealerships:
            if dealer.id == dealer_id:
                context['dealerName'] = dealer.full_name
                context['dealerShortName'] = dealer.short_name
        
        context['cars'] = CarModel.objects.filter(dealer=dealer_id)
        context['dealerID'] = dealer_id
        
        return render(request, 'djangoapp/add_review.html', context)

##'content': ['asdsa'], 'purchasecheck': ['on'], 'car': ['2'], 'purchasedate': ['02/10/2021']}
    if request.method == "POST":
        if request.user.is_authenticated:
            print(request.POST)
            review = {}    
            review["id"] = dealer_id
            review['name'] = request.user.username
            review['dealership'] = dealer_id
            review['review'] = request.POST["content"]
            if "purchasecheck" in request.POST and request.POST["purchasecheck"] == "on":
                review['purchase'] = True
            else:
                review['purchase'] = False
            review['purchase_date'] = datetime.strptime(request.POST["purchasedate"], '%m/%d/%Y').isoformat()
            selected_car = CarModel.objects.get(pk=request.POST['car'])
            review['car_make'] = selected_car.make.name
            review['car_model'] = selected_car.name
            review['car_year'] = selected_car.year.strftime("%Y")
            json_payload = {}
            json_payload["review"] = review
            url = "https://faimpessoa-5000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
            result = post_request(url, json_payload)
    else:
        result = "You must POST"
    
    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
