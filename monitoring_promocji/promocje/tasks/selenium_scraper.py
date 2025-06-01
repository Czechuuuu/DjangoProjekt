from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from promocje.models import Produkt, HistoriaCen
import re
from django.core.mail import send_mail

def konfiguruj_przegladarke():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(r"C:/WebDrivers/chromedriver.exe")
    return webdriver.Chrome(service=service, options=options)

def wyciagnij_cene_z_tekstu(cena_text):
    cena_text = re.sub(r"[^\d,]", "", cena_text).replace(",", ".")
    return float(cena_text)
    
def pobierz_cene_selenium(url):
    driver = konfiguruj_przegladarke()
    try:
        driver.get(url)

        if "amazon" in url:
            whole_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "a-price-whole"))
            )
            fraction_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "a-price-fraction"))
            )

            whole_part = whole_element.text.strip()
            fraction_part = fraction_element.text.strip()

            cena_text = f"{whole_part}.{fraction_part}"
            return float(cena_text)

        elif "mediaexpert" in url:
            cena_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".main-price.is-big"))
            )
            cena_text = cena_element.get_attribute("mainprice")
            if cena_text:
                return int(cena_text) / 100
            else:
                cena_text = cena_element.text.strip()
                return wyciagnij_cene_z_tekstu(cena_text)

        else:
            raise ValueError("Nieobsługiwany URL. Obsługiwane strony: Amazon, MediaExpert.")

    except Exception as e:
        print(f"Błąd podczas pobierania ceny z URL {url}: {e}")
        return None

    finally:
        driver.quit()

def aktualizuj_ceny_selenium():
    produkty = Produkt.objects.all()
    for produkt in produkty:
        nowa_cena = pobierz_cene_selenium(produkt.url)
        if nowa_cena is not None:
            HistoriaCen.objects.create(produkt=produkt, cena=nowa_cena)

            if nowa_cena <= produkt.cena_docelowa:
                wyslij_powiadomienie(produkt, nowa_cena)

            if produkt.aktualna_cena != nowa_cena:
                produkt.aktualna_cena = nowa_cena
                produkt.save()
                
def wyslij_powiadomienie(produkt, nowa_cena):
    temat = f'Promocja na {produkt.nazwa}!'
    wiadomosc = (
        f'Produkt "{produkt.nazwa}" osiągnął cenę docelową!\n'
        f'Nowa cena: {nowa_cena} zł\n'
        f'Cena docelowa: {produkt.cena_docelowa} zł\n'
        f'Link do produktu: {produkt.url}'
    )
    if produkt.email_odbiorcy:
        send_mail(temat, wiadomosc, 'twoj_email@example.com', [produkt.email_odbiorcy])