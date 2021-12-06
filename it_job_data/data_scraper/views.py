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

#JJIT offers
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
            exp_lvl = slugify(offer['experience_level'])
            #print(f'3)#####{exp_lvl}##### \n')
            company_name = slugify(offer['company_name'])
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
                skills.append(slugify(skill))
            #print(f'7)#####{skills}##### \n')
            offer_obj = Offer.objects.get_or_create(from_site=self.source, offer_id=offer_id)[0]
            offer_obj.add_change(
                    offer_full_link=offer_full_link, position_title=position_title, exp_lvl=exp_lvl, company_name=company_name, skills=skills, 
                    min_salary=int(min_salary), max_salary=int(max_salary))
        
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

#NFJ offers
class NFJOffers:

    BASE_URL = 'https://nofluffjobs.com'

    def __init__(self):
        self.source = 'nofluffjobs.com'
        self.seniority = ['trainee', 'junior', 'mid', 'senior', 'expert']
        self.page_number = 1
        self.max_page_number = 0

    def get_nfj_data(self, seniority, page_nr='1'):
        self.nfj_html = requests.get(f'{self.BASE_URL}/pl/praca-it?criteria=seniority%3D{seniority}&page={page_nr}').text
#parse the html
        self.nfj_webpage = BeautifulSoup(self.nfj_html, 'lxml')

    def pick_max_page(self):
#find out how many pages of results there are and pick the highest number
        page_number_links = self.nfj_webpage.find_all(class_='page-link')
        number_of_pages = []
        for i in range(1, len(page_number_links)-1):
            number = page_number_links[i].text
            try:
                number_of_pages.append(int(number))
            except ValueError:
                print('znak inny niż cyfra')
                return False
            finally:
                continue  
        self.max_page_number = max(number_of_pages)

    def get_offers(self):
#find all the 'offer' items on the page
        self.offers = self.nfj_webpage.find_all('a', class_='posting-list-item')

    def analyze_offers(self, seniority):
#get all the needed information from the offer
        for i in range(0, len(self.offers) + 1):
            try:
                offer = self.offers[i]
                print(f'*****{seniority}:  offer {i}*****')
                offer_id = offer.get('id')
                #print(f'*******{offer_id}******* \n')
                offer_link = offer.get('href')
                offer_full_link = f'https://nofluffjobs.com{offer_link}'
                #print(f'########{offer_full_link}######## \n')
                position_title = offer.find('h3', class_='posting-title__position').text
                #print(f'#######{position_title}########## \n')
                company_name = slugify(offer.find('span', class_='posting-title__company').text.replace('@ ', ''))
                print(f'#######{company_name}########## \n')
                salary = offer.find(class_='salary').text
                try:

                    splitted_salary = salary.replace(' ', '').split('-')
                    min_salary = self.parse_salary(splitted_salary[0])
                    #print(f'#######{min_salary}########## \n')
                    max_salary = self.parse_salary(splitted_salary[1])
                    #print(f'#######{max_salary}########## \n')
                except IndexError:
                    min_salary = -1
                    max_salary = -1            
                    #print('Brak widełek płacowych')
                inside_offer = NFJAnalyzeOffer()
                skills = inside_offer.read_skills(offer_full_link)
                offer_obj = Offer.objects.get_or_create(from_site=self.source, offer_id=offer_id)[0]
                offer_obj.add_change(
                    offer_full_link=offer_full_link, position_title=position_title, exp_lvl=slugify(seniority), company_name=company_name, skills=skills, 
                    min_salary=int(min_salary), max_salary=int(max_salary))
            except Exception as error:
                print(f'{type(error).__name__} was raised: {error}')
                print(traceback.print_exception(error))
            finally:
                continue

    def get_all_offers(self):
        for element in self.seniority:
            seniority = element
            #print(f'for seniority: {element}')
            self.get_nfj_data(seniority)
            self.pick_max_page()
            #print(f'pick max page @@@@@@@@@@@@@@@ max page nr: {self.max_page_number}')
            for page in range(1, int(self.max_page_number) + 1):
                self.get_nfj_data(seniority, page_nr=page)
                #print(f'for page: @@@@@@@@@@@@@ seniority: {seniority} \n @@@@@@@@ page: {page}')                
                self.get_offers()
                self.analyze_offers(seniority)
                time.sleep(random.random()*10 + 5)

    def parse_salary(self, salary):
        return re.sub('[^0-9,\\.]', '', salary) 

class NFJAnalyzeOffer:

    def __init__(self):
        pass

    def read_skills(self, link, ):
        offer_html = requests.get(link).text
        offer_soup = BeautifulSoup(offer_html, 'lxml')
        skills = []
        required = offer_soup.find_all('common-posting-item-tag')
        for i in range(len(required)):
            skill = required[i]
            skills.append(slugify(skill.find(class_='btn').text))
        return skills

def get_offers(request):
    #data_jjit = JJitOffers()
    #data_jjit.analyze_offers()
    data_nfj = NFJOffers()
    data_nfj.get_all_offers()
    response = 'Oferty pobrane do bazy danych'
    return HttpResponse(response)

def home_page(request):
    top_offers = Offer.best_paid_jobs(Offer, 'junior')
    index_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    offer_data = dict(zip(index_list, top_offers))
    return render(request, 'data_scraper/homepage.html', context={'top_offers': offer_data})

def offers_page(request):
    return render(request, 'data_scraper/offers.html')

def newsletter(request):
    return render(request, 'data_scraper/newsletter.html')