from django.db import models

# Create your models here.
class Offers(models.Model):
    offer_id = models.CharField(max_length=50)
    offer_full_link = models.CharField(max_length=200)
    position_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=50)
    min_salary = models.IntegerField()
    max_salary = models.IntegerField()