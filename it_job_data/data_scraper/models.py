from django.db import models

# Create your models here.
EXP_LVL_OPTIONS = [('trainee', 'Stażysta'), ('junior', 'Junior'), ('mid', 'Mid'), ('senior', 'Senior'), ('expert', 'Expert')]
class Offer(models.Model):
    from_site = models.CharField(max_length=100)
    offer_id = models.CharField(max_length=100)
    offer_full_link = models.CharField(max_length=200)
    position_title = models.CharField(max_length=100)
    exp_lvl = models.CharField(max_length=100, choices=EXP_LVL_OPTIONS)
    company_name = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)
    min_salary = models.IntegerField()
    max_salary = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False) 

    def __str__(self):
        return f'Oferta z: {self.from_site},\n {self.offer_full_link} \n'