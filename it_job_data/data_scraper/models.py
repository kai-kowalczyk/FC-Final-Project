from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Offer(models.Model):
    from_site = models.CharField(max_length=100)
    offer_id = models.CharField(max_length=100)
    offer_full_link = models.CharField(max_length=200)
    position_title = models.CharField(max_length=100)
    exp_lvl = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)
    min_salary = models.IntegerField()
    max_salary = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False) 