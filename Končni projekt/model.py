# Uvozimo knjiznjico za delo z datotekami/podatki v formatu JSON
import json

IME_DATOTEKE = 'stanje.json'

# vkljucimo knjiznico, ki generira datume
from datetime import date
danasnji_datum = date.today()
danasnji_datum = danasnji_datum.strftime("%d_%m_%Y")

class Uporabnik:

    def __init__(self):
        self.preberi_stanje()

    def preberi_stanje(self):
        # Ker uporabljamo samo enega uporabnika - nadgradnja na več uporabnikov je seveda mogoča - lahko na začetku preberemo shranjeno stanje
        # Odpremo datoteko, do katere dostopamo v spremenljivki datoteka
            with open(IME_DATOTEKE) as datoteka:
                # Iz nje preberemo podatke in jih vrnemo
                slovar_stanja = json.load(datoteka)

                # V trenutnega uporabnika (ki je zaenkrat edini), shranimo njegovo trenutno operacijo in statistiko pravilno rešenih računov
                self.trenutna_operacija = slovar_stanja['trenutna_operacija']
                self.pravilno_odgovorjeni = slovar_stanja['pravilno_odgovorjeni']
                self.stevilo_poskusov = slovar_stanja['stevilo_poskusov']
                self.dnevna_statistika = slovar_stanja['dnevna_statistika']

                #...
                if danasnji_datum not in self.dnevna_statistika:
                    self.dnevna_statistika[danasnji_datum] ={
                        'pravilno_odgovorjeni': 0,
                        'stevilo_poskusov': 0
                    }

    def shrani_stanje(self):
        # Zgradimo slovar, ki hrani trenutno shranjeno operacijo in statistiko stevila pravilno rešenih računov (za popestritev aplikacije)
        slovar_stanja = {
            'trenutna_operacija': self.trenutna_operacija,
            'pravilno_odgovorjeni': self.pravilno_odgovorjeni,
            'stevilo_poskusov': self.stevilo_poskusov,
            'dnevna_statistika': self.dnevna_statistika
        }

        # Odpremo datoteko, do katere dostopamo v spremenljivki datoteka
        with open(IME_DATOTEKE, 'w') as datoteka:
            # Zgrajeni slovar slovar_stanja zapišemo v datoteko datoteka
            json.dump(slovar_stanja, datoteka, ensure_ascii=False, indent=4)
