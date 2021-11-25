from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('jjit_offers/', views.jjit_offers, name='jjit_scraper'),
]
