from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('produkt/<int:produkt_id>/', views.produkt_szczegoly, name='produkt_szczegoly'),
    path('dodaj/', views.dodaj_produkt, name='dodaj_produkt'),
    path('uruchom-scraper-selenium/', views.uruchom_scraper_selenium, name='uruchom_scraper_selenium'),
]
