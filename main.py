import requests
from bs4 import BeautifulSoup
import json
import random

#JUSTJOIN.IT OFFERS
'''jjit_offers = requests.get('https://justjoin.it/api/offers').json()
for i in range(0, 49):
    print(jjit_offers[i])'''

#NOFLUFFJOBS.COM OFFERS
class NFJOffers:

    BASE_URL = 'https://nofluffjobs.com'

    def __init__(self):
        self.seniority = ['trainee', 'junior', 'mid', 'senior', 'expert']
        self.page_number = 1
        self.max_page_number = 0

    def request_nfj_data(self):
        self.nfj_html = requests.get(f'{self.BASE_URL}/pl/praca-it?criteria=seniority%3D{self.seniority[0]}&page={self.page_number}').text
        #parse the html
        self.nfj_webpage = BeautifulSoup(self.nfj_html, 'lxml')

    def everything_else(self):
#find out how many pages of results there are and pick the highest number
        page_number_links = self.nfj_webpage.find_all(class_='page-link')
        number_of_pages = []
        for i in range(1, len(page_number_links)-1):
            number_of_pages.append(page_number_links[i].text)
            self.max_page_number = max(number_of_pages)

#find all the 'offer' items on the page
        offers = self.nfj_webpage.find_all('a', class_='posting-list-item')

#get all the needed information from the offer
        for i in range(1,6):
            offer = offers[i]
            offer_id = offer.get('id')
            print(f'#######{offer_id}########## \n')
            offer_link = offer.get('href')
            offer_full_link = f'https://nofluffjobs.com{offer_link}'
            print(f'########{offer_full_link}######## \n')
            position_title = offer.find('h3', class_='posting-title__position').text
            print(f'#######{position_title}########## \n')
            company_name = offer.find('span', class_='posting-title__company').text
            print(f'#######{company_name}########## \n')
            salary = offer.find(class_='salary' ).text
            print(f'#######{salary}########## \n')
            offer_html = requests.get(offer_full_link).text
            offer_parser = BeautifulSoup(offer_html, 'lxml')
            skills = []
            required = offer_parser.find_all('common-posting-item-tag')
            for i in range(len(required)):
                skill = required[i]
                skills.append(skill.find(class_='btn').text)
            print(f'#######{skills}########## \n')


nfj = NFJOffers()
nfj.request_nfj_data()
nfj.everything_else()