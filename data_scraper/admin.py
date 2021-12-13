from django.contrib import admin
from data_scraper.models import Offer
# Register your models here.

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['offer_id', 'from_site', 'position_title', 'exp_lvl', 'company_name', 'min_salary', 'max_salary']
    list_editable = ['min_salary', 'max_salary']
