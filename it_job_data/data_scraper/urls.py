from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('get_offers/', views.get_offers, name='offers_scraper'),
]
