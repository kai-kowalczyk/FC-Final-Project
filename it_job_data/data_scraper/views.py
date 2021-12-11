from django.shortcuts import render
from django.http import HttpResponse
from .models import Offer
import requests
from bs4 import BeautifulSoup
import random
import time
import traceback
import re
from django.utils.text import slugify

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the data_scraper index.")

def home_page(request):
    top_offers = Offer.best_paid_jobs(Offer, 'junior')
    index_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    offer_data = dict(zip(index_list, top_offers))
    return render(request, 'data_scraper/homepage.html', context={'top_offers': offer_data})

def offers_page(request):
    return render(request, 'data_scraper/offers.html')

def newsletter(request):
    return render(request, 'data_scraper/newsletter.html')