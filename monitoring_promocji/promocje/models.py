from django.db import models

class Produkt(models.Model):
    nazwa = models.CharField(max_length=255)
    url = models.URLField()
    aktualna_cena = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cena_docelowa = models.DecimalField(max_digits=10, decimal_places=2)
    ostatnia_aktualizacja = models.DateTimeField(auto_now=True)
    email_odbiorcy = models.EmailField(default='default@example.com')

    def __str__(self):
        return self.nazwa

class HistoriaCen(models.Model):
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE, related_name="historia")
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    data_sprawdzenia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.produkt.nazwa}: {self.cena} zł ({self.data_sprawdzenia})"
