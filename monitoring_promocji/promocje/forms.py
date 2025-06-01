from django import forms
from .models import Produkt

class ProduktForm(forms.ModelForm):
    class Meta:
        model = Produkt
        fields = ['nazwa', 'url', 'cena_docelowa', 'email_odbiorcy']