from django.db import models

# Create your models here.
EXP_LVL_OPTIONS = [('trainee', 'Stażysta'), ('junior', 'Junior'), ('mid', 'Mid'), ('senior', 'Senior'), ('expert', 'Expert')]

FROM_SITE = [('justjoin.it', 'justjoin.it'), ('nofluffjobs.com', 'NoFluffJobs')]
class Offer(models.Model):
    from_site = models.CharField(max_length=20, choices=FROM_SITE)
    offer_id = models.CharField(max_length=100)
    offer_full_link = models.CharField(max_length=200)
    position_title = models.CharField(max_length=100)
    exp_lvl = models.CharField(max_length=10, choices=EXP_LVL_OPTIONS)
    company_name = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)
    min_salary = models.IntegerField(default=0)
    max_salary = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False) 

    def add_change(self, offer_full_link, position_title, exp_lvl, company_name, skills, min_salary, max_salary):
        print(offer_full_link, position_title, exp_lvl, company_name, skills, min_salary, max_salary)
        self.offer_full_link = offer_full_link
        self.position_title = position_title
        self.exp_lvl = exp_lvl
        self.company_name = company_name
        self.skills = skills
        self.min_salary = min_salary
        self.max_salary = max_salary
        self.save()
        changed_offer = OfferChanges(
            offer=self, 
            position_title=position_title,
            exp_lvl=exp_lvl,
            skills=skills,
            min_salary=min_salary,
            max_salary=max_salary
        )
        changed_offer.save()

    def __str__(self):
        return f'Oferta z: {self.from_site}, {self.offer_full_link}'

class OfferChanges(models.Model):
    offer = models.ForeignKey(Offer, related_name='offer_changes', on_delete=models.CASCADE)
    position_title = models.CharField(max_length=100)
    exp_lvl = models.CharField(max_length=10, choices=EXP_LVL_OPTIONS)
    skills = models.CharField(max_length=200)
    min_salary = models.IntegerField()
    max_salary = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)