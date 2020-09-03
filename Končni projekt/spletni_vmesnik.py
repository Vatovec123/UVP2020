from datetime import date
import bottle
import os
import random
from model import Uporabnik

# vkljucimo knjiznico, ki generira datume
from datetime import date
danasnji_datum = date.today()
danasnji_datum = danasnji_datum.strftime("%d_%m_%Y")


uporabnik = Uporabnik()


def preusmeri_na_opcijo(opcija):
    if opcija is 1:
        bottle.redirect('/sestevanje')
    elif opcija is 2:
        bottle.redirect('/odstevanje')
    elif opcija is 3:
        bottle.redirect('/mnozenje')



@bottle.get('/')
def zacetna_stran():
    opcija = uporabnik.trenutna_operacija
    if opcija is 1:
        ime_shranjene_opcije = 'Seštevanje'
    elif opcija is 2:
        ime_shranjene_opcije = 'Odštevanje'
    elif opcija is 3:
        ime_shranjene_opcije = 'Množenje'
    return bottle.template('index.html', ime_shranjene_opcije=ime_shranjene_opcije,
                                        pravilno_odgovorjeni=uporabnik.pravilno_odgovorjeni,
                                        stevilo_poskusov=uporabnik.stevilo_poskusov)

@bottle.get('/statistika')
def zacetna_stran():
    return bottle.template('statistika.html', dnevna_statistika=uporabnik.dnevna_statistika)



@bottle.get('/preusmeri_na_shranjeno_opcijo')
def preusmeri_na_shranjeno_opcijo():
    preusmeri_na_opcijo(uporabnik.trenutna_operacija)


@bottle.get('/sestevanje')
def sestevanje():
    # Shranimo, da trenutni uporabnik utrjuje seštevanje
    uporabnik.trenutna_operacija = 1
    uporabnik.shrani_stanje()

    # Zgeneriramo stevili in ju pošljemo uporabiku, ob tem, da vemo, da ju bo moral sešteti
    stevilo1 = random.randint(1, 10)
    stevilo2 = random.randint(1, 10)

    # Odgovora ne pošljemo uporabniku, saj nočemo, da ga lahko kje na strani najde
    # Pravilnost bomo preverili na strežniku v metodi preveri()
    return bottle.template('sestevanje.html', stevilo1=stevilo1, stevilo2=stevilo2)


@bottle.get('/odstevanje')
def odstevanje():
    # Shranimo, da trenutni uporabnik utrjuje odštevanje
    uporabnik.trenutna_operacija = 2
    uporabnik.shrani_stanje()

    # Zgeneriramo stevili in ju pošljemo uporabiku, ob tem, da vemo, da ju bo moral sešteti
    stevilo1 = random.randint(1, 10)
    stevilo2 = random.randint(1, 10)

    # Odgovora ne pošljemo uporabniku, saj nočemo, da ga lahko kje na strani najde
    # Pravilnost bomo preverili na strežniku v metodi preveri()
    return bottle.template('odstevanje.html', stevilo1=stevilo1, stevilo2=stevilo2)


@bottle.get('/mnozenje')
def mnozenje():
    # Shranimo, da trenutni uporabnik utrjuje množenje
    uporabnik.trenutna_operacija = 3
    uporabnik.shrani_stanje()

    # Zgeneriramo stevili in ju pošljemo uporabiku, ob tem, da vemo, da ju bo moral sešteti
    stevilo1 = random.randint(1, 10)
    stevilo2 = random.randint(1, 10)

    # Odgovora ne pošljemo uporabniku, saj nočemo, da ga lahko kje na strani najde
    # Pravilnost bomo preverili na strežniku v metodi preveri()
    return bottle.template('mnozenje.html', stevilo1=stevilo1, stevilo2=stevilo2)


@bottle.get('/pravilen_odgovor')
def pravilen_odgovor():
    return bottle.template('pravilen_odgovor.html')


@bottle.get('/napacen_odgovor')
def napacen_odgovor():
    return bottle.template('napacen_odgovor.html')


@bottle.post('/preveri')
def preveri():
    # Uporabniku prištejemo trenutni poskus k skupnem številu
    uporabnik.stevilo_poskusov += 1
    uporabnik.dnevna_statistika[danasnji_datum]['stevilo_poskusov'] += 1

    # Uporabnik k zahtevku priloži števili, s katerimi je operiral
    stevilo1 = int(bottle.request.forms['stevilo1'])
    stevilo2 = int(bottle.request.forms['stevilo2'])

    # In operacijo, ki jo je uporabil
    operacija = bottle.request.forms['operacija']

    # Prilozi tudi njegov rezultat, ki ga je izračunal sam
    rezultat = int(bottle.request.forms['rezultat'])

    if operacija == "sestevanje":
        odgovor = stevilo1 + stevilo2
    elif operacija == "odstevanje":
        odgovor = stevilo1 - stevilo2
    else:
        odgovor = stevilo1 * stevilo2

    if rezultat == odgovor:
        uporabnik.pravilno_odgovorjeni += 1
        uporabnik.dnevna_statistika[danasnji_datum]['pravilno_odgovorjeni'] += 1

        # Usmerimo uporabnika na prikaz sporočila, da je odgovoril pravilno
        bottle.redirect('/pravilen_odgovor')

    # Shranimo uporabnikovo stanje v datoteko
    uporabnik.shrani_stanje()

    # Usmerimo uporabnika na prikaz sporočila, da je odgovoril napačno
    bottle.redirect('/napacen_odgovor')


@bottle.get('/pomoc')
def pomoc():
    return bottle.template('pomoc.html')


bottle.run(debug=True, reloader=True)
