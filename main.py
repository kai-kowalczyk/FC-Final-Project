import requests
from bs4 import BeautifulSoup
import json
import random

#JUSTJOIN.IT OFFERS
class JJitOffers:

    BASE_URL = 'https://justjoin.it/api/offers'

    def __init__(self):
        self.jjit_offers = self.get_offers()

    def get_offers(self):
        return requests.get('https://justjoin.it/api/offers').json()
        

    def analyze_offers(self):  
        for i in range(0,10):
            offer = self.jjit_offers[i]
            #print(offer)
            offer_id = offer['id']
            print(f'******{offer_id}****** \n')
            offer_full_link = f'https://justjoin.it/offers/{offer_id}'
            #print(f'#####{offer_full_link}##### \n')
            position_title = offer['title']
            #print(f'#####{position_title}##### \n')
            exp_lvl = offer['experience_level']
            #print(f'#####{exp_lvl}##### \n')
            company_name = offer['company_name']
            #print(f'#####{company_name}##### \n')
            min_salary = self.path(offer, 'employment_types.0.salary.from', 'undisclosed min_salary')
            min_salary2 = offer['employment_types'][0]['salary']['from']
            print(f'#####{min_salary}##### \n')
            print(min_salary2)
            max_salary = self.path(offer, 'employment_types.0.salary.to', 'undisclosed max_salary')
            max_salary2 = offer['employment_types'][0]['salary']['to']
            print(f'#####{max_salary}##### \n')
            print(max_salary2)
            skills = []
            for i in range(len(offer['skills'])):
                skill = offer['skills'][i]['name']
                skills.append(skill)
            #print(f'#####{skills}##### \n')
        '''except Exception as error:
            print(f'{type(error).__name__} was raised: {error}')
        finally:
            continue'''

            #SALARY
            #'employment_types': [{'type': 'permanent', 'salary': None}, {'type': 'b2b', 'salary': None}]
            #'employment_types': [{'type': 'permanent', 'salary': {'from': 14000, 'to': 18000, 'currency': 'pln'}}]
            #'employment_types': [{'type': 'b2b', 'salary': {'from': 13000, 'to': 22000, 'currency': 'pln'}}]
            #'employment_types': [{'type': 'b2b', 'salary': {'from': 6000, 'to': 7000, 'currency': 'eur'}}]
            #'employment_types': [{'type': 'b2b', 'salary': {'from': 7000, 'to': 9500, 'currency': 'pln'}}, {'type': 'permanent', 'salary': {'from': 6000, 'to': 8000, 'currency': 'pln'}}]

    def path(self, root, p, d):
        curr = root
        for piece in p.split('.'):
            print(piece)
            if isinstance(curr, dict) and piece in curr:
                print('piece in curr')
                curr = curr[piece]
            elif isinstance(curr, list) and len(curr) > int(piece):
                curr = curr[int(piece)]
            else:
                print('else')
                return d
        return curr
        
            



#NOFLUFFJOBS.COM OFFERS
class NFJOffers:

    BASE_URL = 'https://nofluffjobs.com'

    def __init__(self):
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
            number_of_pages.append(page_number_links[i].text)   
        self.max_page_number = int(max(number_of_pages))

    def get_offers(self):
#find all the 'offer' items on the page
        self.offers = self.nfj_webpage.find_all('a', class_='posting-list-item')

    def analyze_offers(self):
#get all the needed information from the offer
        for i in range(0,10):
            try:
                offer = self.offers[i]
                offer_id = offer.get('id')
                print(f'*******{offer_id}******* \n')
                offer_link = offer.get('href')
                offer_full_link = f'https://nofluffjobs.com{offer_link}'
                #print(f'########{offer_full_link}######## \n')
                position_title = offer.find('h3', class_='posting-title__position').text
                #print(f'#######{position_title}########## \n')
                company_name = offer.find('span', class_='posting-title__company').text
                #print(f'#######{company_name}########## \n')
                salary = offer.find(class_='salary' ).text
                splitted_salary = salary.split(' - ')
                min_salary = splitted_salary[0]
                print(f'#######{min_salary}########## \n')
                max_salary = splitted_salary[1]
                print(f'#######{max_salary}########## \n')

                inside_offer = NFJAnalyzeOffer()
                skills = inside_offer.read_skills(offer_full_link)
                '''offer_html = requests.get(offer_full_link).text
                inside_offer = BeautifulSoup(offer_html, 'lxml')
                skills = []
                required = inside_offer.find_all('common-posting-item-tag')
                for i in range(len(required)):
                    skill = required[i]
                    skills.append(skill.find(class_='btn').text)'''
                #print(f'#######{skills}########## \n')
            except Exception as error:
                print(f'{type(error).__name__} was raised: {error}')
            finally:
                continue

    def get_all_offers(self):
        for element in self.seniority:
            seniority = element
            self.get_nfj_data(seniority)
            self.pick_max_page()
            for page in range(1, self.max_page_number + 1):
                self.get_nfj_data(seniority, page_nr=page)
                self.get_offers()
                self.analyze_offers()

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
            skills.append(skill.find(class_='btn').text)
        return skills
        print(f'#######{skills}########## \n')
                


#nfj = NFJOffers()
#nfj.get_all_offers()

jjit = JJitOffers()
jjit.analyze_offers()