from django.core.management.base import BaseCommand, CommandError
from ...models import Offer
from data_scraper.script.offers_scraper import NFJOffers, JJitOffers
import traceback

class Command(BaseCommand):
    help = 'Runs a script that scrapes and parses through job offers from nofluffjobs.com & justjoin.it.'

    def handle(self, *args, **options):
        try:
            data_jjit = JJitOffers()
            data_jjit.analyze_offers()
            data_nfj = NFJOffers()
            data_nfj.get_all_offers()
        except Exception as error:
            print(traceback.print_exception(error))
        self.stdout.write(self.style.SUCCESS('Succesfully scraped the websites and added data to database.'))
