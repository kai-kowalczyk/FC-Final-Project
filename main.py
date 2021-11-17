import requests
from bs4 import BeautifulSoup
import json
import random

#justjoin.it offers
'''jjit_offers = requests.get('https://justjoin.it/api/offers').json()
for i in range(0, 49):
    print(jjit_offers[i])'''

#nofluffjobs.com offers
seniority = ['trainee', 'junior', 'mid', 'senior', 'expert']
page_nr = 1

nfj_html = requests.get(f'https://nofluffjobs.com/pl/praca-it?criteria=seniority%3D{seniority[0]}&page={page_nr}').text
nfj_webpage = BeautifulSoup(nfj_html, 'lxml')
offer = nfj_webpage.find('a', class_='posting-list-item')
position_title = offer.find('h3', class_='posting-title__position').text
print(position_title)
offer_id = offer.a.id.text
print(offer_id)

#print(offer.prettify())
#print(nfj_webpage.prettify())


