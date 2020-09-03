# vklučimo knjižnico, ki nam generira naključna števila
import random

# vključimo model uporabnika
from model import Uporabnik


# vkljucimo knjiznico, ki generira datume
from datetime import date
danasnji_datum = date.today()
danasnji_datum = danasnji_datum.strftime("%d_%m_%Y")

# zgradimo uporabnika, ki sam prebere datoteko s svojim stanjem
uporabnik = Uporabnik()


def uvod(uporabnik):
    naslov = '====Utrjevanje osnovnih računskih operacij za otroke=='
    print('=' * len(naslov))
    print(naslov)
    print("=" * len(naslov))

    prikaz_rezultatov(uporabnik)


def kazalo():
    poglavja = ['1.Seštevanje', '2.Odštevanje', '3.Množenje', '4.Izhod']
    print(poglavja[0])
    print(poglavja[1])
    print(poglavja[2])
    print(poglavja[3])


def razmik():
    print('=' * 29)


def izbira_poglavja():
    izbira = int(input('Vstavi svojo izbiro:'))
    while izbira > 4 or izbira <= 0:
        print('Te možnosti nimaš na izbiro.')
        izbira = int(input('Prosim poskusi še enkrat.'))
    else:
        return izbira


def postavljeno_vprašanje(vprasanje):
    print('Vpiši svoj odgovor (ali vpiši x za vrnitev v glavni meni): ')
    print(vprasanje, end='')

    rezultat = input('=')

    # Če uporabnik vpiše x, namesto števila vrnemo None, kar bo naznanilo, da moramo program vrniti v glavni meni
    if rezultat is 'x':
        return None

    # Drugače pa pretvorimo vhod v celo število
    rezultat = int(rezultat)

    return rezultat


def preveri_rezultat(rezultat, odgovor):
    if rezultat == odgovor:
        print('Pravilno.')
        return True
    else:
        print('Narobe.')
        return False


def moznost_izbire(indeks):

    stevilo1 = random.randint(1, 10)
    stevilo2 = random.randint(1, 10)

    if indeks is 1:
        vprasanje = str(stevilo1) + '+' + str(stevilo2)
        odgovor = stevilo1 + stevilo2

    elif indeks is 2:
        vprasanje = str(stevilo1) + '-' + str(stevilo2)
        odgovor = stevilo1 - stevilo2

    else:
        vprasanje = str(stevilo1) + '*' + str(stevilo2)
        odgovor = stevilo1 * stevilo2

    rezultat = postavljeno_vprašanje(vprasanje)

    # Če je uporabnik namesto rezultata vnesel x, vrnemo None, saj želimo programu sporočiti, naj se vrne na začetni meni
    if rezultat is None:
        return None

    # Če pa je vnesel rezultat, ga preverimo
    rezultat_je_pravilen = preveri_rezultat(rezultat, odgovor)

    return rezultat_je_pravilen

# Za uporabnika uporabnik prikažemo statistiko


def prikaz_rezultatov(uporabnik):
    print('Statistika')

    print('Število računov:', uporabnik.stevilo_poskusov)
    print('Število pravilnih odgovorov:', uporabnik.pravilno_odgovorjeni)
    print('Kako nam je šlo danes:', uporabnik.dnevna_statistika)


def glavno():

    uvod(uporabnik)
    razmik()

    # Naložimo trenutno izbrano operacijo, ki jo treniramo, iz datoteke
    opcija = uporabnik.trenutna_operacija

    # Dokler uporabnik ne izbere opcije izhod
    while opcija != 4:

        # Če opcija ni izhod, jo shranimo v stanje, da bo naslednjič avtomatsko naložena
        uporabnik.trenutna_operacija = opcija

        # Nastavimo pravilen rezultat na neko začetno vrednost, ki zaenkrat ni pomembna
        pravilen_rezultat = False

        # Dokler ne vpišemo x kot rezultata (oziroma dokler moznost_izbire ne vrne None) ponujamo nova vprašanja
        while pravilen_rezultat is not None:

            # Pogledamo, če je rezultat pravilen ali pa če je morda uporabnik želel zamenjati operacijo
            pravilen_rezultat = moznost_izbire(opcija)

            if pravilen_rezultat:
                # Rezultat je pravilen, dodamo ena k pravilno odgovorjenim vprasanjem uporabnika,
                # zanka pa gre naprej v nov obhod in ponudi nov račun iste operacije
                uporabnik.pravilno_odgovorjeni += 1
                uporabnik.dnevna_statistika[danasnji_datum]['pravilno_odgovorjeni'] += 1

            if pravilen_rezultat is not None:
                # Če uporabnik ne želi prekiniti poskusa in se vrniti v meni,
                # dodamo en poskus v statistiko
                uporabnik.stevilo_poskusov += 1
                uporabnik.dnevna_statistika[danasnji_datum]['stevilo_poskusov'] += 1

            # Nadaljujemo zanko, ki ponudi novo moznost izbire (vpisovanje rezultata, vrstica 118)
            # Če je pravilen_rezultat slučajno None, se bo notranja zanka prenehala izvajati,
            # zunanja zanka pa bo ponudila novo izbiro_poglavja (vrstica 128)

        razmik()
        kazalo()
        razmik()

        opcija = izbira_poglavja()

    # Ob izhodu iz programa shranimo in prikazemo statistiko
    uporabnik.shrani_stanje()
    razmik()
    prikaz_rezultatov(uporabnik)


glavno()
