from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('jjit_offers/', views.jjit_offers, name='jjit_scraper')
]
