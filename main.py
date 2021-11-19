import requests
from bs4 import BeautifulSoup
import json
import random

#JUSTJOIN.IT OFFERS
jjit_offers = requests.get('https://justjoin.it/api/offers').json()
for i in range(0, 49):
    print(jjit_offers[i])

#NOFLUFFJOBS.COM OFFERS
seniority = ['trainee', 'junior', 'mid', 'senior', 'expert']
page_number = 1

nfj_html = requests.get(f'https://nofluffjobs.com/pl/praca-it?criteria=seniority%3D{seniority[0]}&page={page_number}').text

nfj_webpage = BeautifulSoup(nfj_html, 'lxml')
page_number_links = nfj_webpage.find_all(class_='page-link')
number_of_pages = []
for i in range(1, len(page_number_links)-1):
    number_of_pages.append(page_number_links[i].text)
max_page_number = max(number_of_pages)
offers = nfj_webpage.find_all('a', class_='posting-list-item')
for i in range(len(offers)):
    offer = offers[i]
    offer_id = offer.get('id')
    print(offer_id)
    offer_link = offer.get('href')
    print(f'https://nofluffjobs.com{offer_link}')
    position_title = offer.find('h3', class_='posting-title__position').text
    print(position_title)
    company_name = offer.find('span', class_='posting-title__company').text
    print(company_name)
    salary = offer.find(class_='salary' ).text
    print(salary)
    



    

#print(offers.prettify())
#print(nfj_webpage.prettify())


