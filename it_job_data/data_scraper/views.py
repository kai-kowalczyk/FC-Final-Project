from django.shortcuts import render
from django.http import HttpResponse
from .models import Offer
import requests
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the data_scraper index.")


class JJitOffers:

    BASE_URL = 'https://justjoin.it/api/offers'

    def __init__(self):
        self.source = 'justjoin.it'
        self.jjit_offers = self.get_offers()

    def get_offers(self):
        return requests.get('https://justjoin.it/api/offers').json()
        

    def analyze_offers(self):  
        for i in range(0, len(self.jjit_offers)):
            offer = self.jjit_offers[i]
            #print(offer)
            print(f'@@@@@@@@@ NUMER OFERTY {i} @@@@@@@@@@@@@@')
            offer_id = offer['id']
            #print(f'******{offer_id}****** \n')
            offer_full_link = f'https://justjoin.it/offers/{offer_id}'
            #print(f'1)###{offer_full_link}### \n')
            position_title = offer['title']
            #print(f'2)#####{position_title}##### \n')
            exp_lvl = offer['experience_level']
            #print(f'3)#####{exp_lvl}##### \n')
            company_name = offer['company_name']
            #print(f'4)#####{company_name}##### \n')
            min_salary = self.path(offer, 'employment_types.0.salary.from', -1)
            #min_salary2 = offer['employment_types'][0]['salary']['from']
            #print(f'5)#####{min_salary}##### \n')
            #print(min_salary2)
            max_salary = self.path(offer, 'employment_types.0.salary.to', -1)
            #max_salary2 = offer['employment_types'][0]['salary']['to']
            #print(f'6)#####{max_salary}##### \n')
            #print(max_salary2)
            if min_salary == -1 or max_salary == -1:
                min_salary = self.path(offer, 'employment_types.1.salary.from', -1)
                #print(f'5)#####{min_salary}##### \n')
                max_salary = self.path(offer, 'employment_types.1.salary.to', -1)
                #print(f'6)#####{max_salary}##### \n')
            skills = []
            for i in range(len(offer['skills'])):
                skill = offer['skills'][i]['name']
                skills.append(skill)
            #print(f'7)#####{skills}##### \n')
            Offer.objects.get_or_create(from_site=self.source, offer_id=offer_id, offer_full_link=offer_full_link, position_title=position_title, exp_lvl=exp_lvl, company_name=company_name, skills=skills, min_salary=int(min_salary), max_salary=int(max_salary))
        
    def path(self, root, p, d):
        curr = root
        for piece in p.split('.'):
            #print(piece)
            if isinstance(curr, dict) and piece in curr:
                #print('path - piece in curr - dict')
                curr = curr[piece]
            elif isinstance(curr, list) and len(curr) > int(piece):
                #print('path - piece in curr - list')
                curr = curr[int(piece)]
            else:
                #print('path else')
                return d
        return curr

def jjit_offers(request):
    data = JJitOffers()
    data.analyze_offers()
    response = Offer.objects.all()
    return HttpResponse(response)

def home_page(request):
    return render(request, 'data_scraper/homepage.html', context={'name':'world'})