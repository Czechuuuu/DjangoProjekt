from django.contrib import admin
from .models import Produkt, HistoriaCen

@admin.register(Produkt)
class ProduktAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'aktualna_cena', 'ostatnia_aktualizacja')

@admin.register(HistoriaCen)
class HistoriaCenAdmin(admin.ModelAdmin):
    list_display = ('produkt', 'cena', 'data_sprawdzenia')
