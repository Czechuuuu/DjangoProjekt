from django.shortcuts import render, get_object_or_404, redirect
from .models import Produkt
from .forms import ProduktForm
from promocje.tasks.selenium_scraper import aktualizuj_ceny_selenium, pobierz_cene_selenium

def uruchom_scraper_selenium(request):
    aktualizuj_ceny_selenium()
    return redirect('index')

def index(request):
    produkty = Produkt.objects.all()
    return render(request, 'index.html', {'produkty': produkty})

def produkt_szczegoly(request, produkt_id):
    produkt = get_object_or_404(Produkt, id=produkt_id)
    historia_cen = produkt.historia.order_by('-data_sprawdzenia')
    return render(request, 'produkt_szczegoly.html', {'produkt': produkt, 'historia_cen': historia_cen})

def dodaj_produkt(request):
    if request.method == 'POST':
        form = ProduktForm(request.POST)
        if form.is_valid():
            produkt = form.save(commit=False)
            aktualna_cena = pobierz_cene_selenium(produkt.url)
            produkt.aktualna_cena = aktualna_cena
            produkt.save()
            return redirect('index')
    else:
        form = ProduktForm()
    return render(request, 'dodaj_produkt.html', {'form': form})