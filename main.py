import requests
from bs4 import BeautifulSoup
import random
import time

#JUSTJOIN.IT OFFERS
class JJitOffers:

    BASE_URL = 'https://justjoin.it/api/offers'

    def __init__(self):
        self.source = 'justjoin.it'
        self.jjit_offers = self.get_offers()

    def get_offers(self):
        return requests.get('https://justjoin.it/api/offers').json()
        

    def analyze_offers(self):  
        for i in range(0,50):
            offer = self.jjit_offers[i]
            #print(offer)
            print(f'@@@@@@@@@ NUMER {i} @@@@@@@@@@@@@@')
            offer_id = offer['id']
            print(f'******{offer_id}****** \n')
            offer_full_link = f'https://justjoin.it/offers/{offer_id}'
            print(f'1)###{offer_full_link}### \n')
            position_title = offer['title']
            print(f'2)#####{position_title}##### \n')
            exp_lvl = offer['experience_level']
            print(f'3)#####{exp_lvl}##### \n')
            company_name = offer['company_name']
            print(f'4)#####{company_name}##### \n')
            min_salary = self.path(offer, 'employment_types.0.salary.from', 'undisclosed min_salary')
            #min_salary2 = offer['employment_types'][0]['salary']['from']
            #print(f'5)#####{min_salary}##### \n')
            #print(min_salary2)
            max_salary = self.path(offer, 'employment_types.0.salary.to', 'undisclosed max_salary')
            #max_salary2 = offer['employment_types'][0]['salary']['to']
            #print(f'6)#####{max_salary}##### \n')
            #print(max_salary2)
            if min_salary == 'undisclosed min_salary' or max_salary == 'undisclosed min_salary':
                min_salary = self.path(offer, 'employment_types.1.salary.from', 'undisclosed min_salary2')
                print(f'5)#####{min_salary}##### \n')
                max_salary = self.path(offer, 'employment_types.1.salary.to', 'undisclosed max_salary2')
                print(f'6)#####{max_salary}##### \n')
            skills = []
            for i in range(len(offer['skills'])):
                skill = offer['skills'][i]['name']
                skills.append(skill)
            print(f'7)#####{skills}##### \n')
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
                print('path - piece in curr - dict')
                curr = curr[piece]
            elif isinstance(curr, list) and len(curr) > int(piece):
                print('path - piece in curr - list')
                curr = curr[int(piece)]
            else:
                print('path else')
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
            number = page_number_links[i].text
            try:
                number_of_pages.append(int(number))
            except ValueError:
                print('znak inny niż cyfra')
                return False
            finally:
                continue
        print(number_of_pages)  
        self.max_page_number = max(number_of_pages)
        print(self.max_page_number)
        print(type(self.max_page_number))

    def get_offers(self):
#find all the 'offer' items on the page
        self.offers = self.nfj_webpage.find_all('a', class_='posting-list-item')

    def analyze_offers(self, seniority):
#get all the needed information from the offer
        for i in range(0, len(self.offers) + 1):
            try:
                offer = self.offers[i]
                offer_seniority = seniority
                offer_id = offer.get('id')
                print(f'*******{offer_id}******* \n')
                print(f'######{offer_seniority}######')
                offer_link = offer.get('href')
                offer_full_link = f'https://nofluffjobs.com{offer_link}'
                #print(f'########{offer_full_link}######## \n')
                position_title = offer.find('h3', class_='posting-title__position').text
                print(f'#######{position_title}########## \n')
                company_name = offer.find('span', class_='posting-title__company').text
                #print(f'#######{company_name}########## \n')
                salary = offer.find(class_='salary' ).text
                try:
                    splitted_salary = salary.split(' - ')
                    min_salary = splitted_salary[0].replace('', '')
                    #print(f'#######{min_salary}########## \n')
                    max_salary = splitted_salary[1].replace('', '')
                    #print(f'#######{max_salary}########## \n')
                except IndexError: 
                    min_salary = -1
                    max_salary = -2           
                    print('Brak widełek płacowych')
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
            print(f'for seniority: {element}')
            self.get_nfj_data(seniority)
            self.pick_max_page()
            print(f'pick max page @@@@@@@@@@@@@@@ max page nr: {self.max_page_number}')
            for page in range(1, int(self.max_page_number) + 1):
                self.get_nfj_data(seniority, page_nr=page)
                print(f'for page: @@@@@@@@@@@@@ seniority: {seniority} \n @@@@@@@@ page: {page}')                
                self.get_offers()
                self.analyze_offers(seniority)
                time.sleep(random.random() * 10 + 5)

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
                


nfj = NFJOffers()
#nfj.get_nfj_data(seniority='trainee')
#nfj.pick_max_page()
nfj.get_all_offers()

#jjit = JJitOffers()
#jjit.analyze_offers()