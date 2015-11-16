""" AT sirk icin sozluk modulu
Orijinal at'a sadik kalinarak rastgele bir sozlukten alinan
entrylerden rastgele bir tanesi gosterimektedir.
"""

# TODO: command'in sozluk'u bundan daha ustun. Eger hic bir sey bulamazsa
#       eksiden 'bunu mu demek istemistiniz' dedigi linkleri takip ediyor.
#       Boyle bir fonksiyon eklenebilir. Ayrica command'in sozlugu her seye
#       laf yetistirebiliyor. Bu daha cabuk tikaniyor. Belki eksinin linkleri
#       takip edilerek cozulebilir.

import re
import random
import requests
from collections import Counter
from bs4 import BeautifulSoup
from sopel import module


def inci(sorgu):
    r = requests.get('http://www.incisozluk.com.tr/',
                     params={'k': sorgu, 'ce': 'goster'})
    soup = BeautifulSoup(r.text, 'html.parser')
    entryler = soup.find_all('li', {'class': 'entry'})
    if not entryler:
        return None
    return (random.choice(entryler).find('div', {'class': 'entry-text-wrap'})
                                   .get_text().strip())


def eksi(sorgu, follow=True):
    r = requests.get('https://eksisozluk.com/' + sorgu)
    soup = BeautifulSoup(r.text, 'html.parser')
    entry_list = soup.find(id='entry-list')
    # Eger hic entry yoksa 'bunu mu demek istemistiniz'
    # baglantisi takip ediliyor
    if not entry_list and follow:
        suggested = soup.find('a', {'class': 'suggested-title'})
        if suggested:
            return eksi(suggested.get('href'), False)
    if not entry_list:
        return None
    entryler = entry_list.find_all('li')
    return (random.choice(entryler).find('div', {'class': 'content'})
                                   .get_text().strip())


def uludag(sorgu):
    r = requests.get('http://www.uludagsozluk.com/k/' + sorgu)
    soup = BeautifulSoup(r.text, 'html.parser')
    entry_list = soup.find('ol', {'class': 'entry-list'})
    if not entry_list:
        return None
    entryler = entry_list.find_all('div', {'class': 'entry'})
    return (random.choice(entryler).find('div', {'class': 'entry-p'})
                                   .get_text().strip())


def cevap_ver(cevap, bot, trigger):
    if cevap:
        bot.reply(cevap)
    else:
        bot.reply('yok boyle bisi')


@module.commands('eksi')
@module.example('.eksi debian')
def eksi_komutu(bot, trigger):
    """Eksisozlukten bisey getir"""
    cevap_ver(eksi(trigger.group(2)), bot, trigger)


@module.commands('inci')
@module.example('.inci debian')
def inci_komutu(bot, trigger):
    """Incisozlukten bisey getir"""
    cevap_ver(inci(trigger.group(2)), bot, trigger)


@module.commands('ulu')
@module.commands('uludag')
@module.example('.uludag debian')
def ulu_komutu(bot, trigger):
    """Uludagsozlukten bisey getir"""
    cevap_ver(uludag(trigger.group(2)), bot, trigger)


@module.rule('.+ $nickname')
@module.rule('$nickname[ !?,.:].+')
def sozluk(bot, trigger):
    # gecen cumle icinden botun adini cikar
    sorgu = trigger.replace(bot.nick, '').strip()

    # eger sorguda cok fazla kelime geciyorsa
    # sadece 1 tanesini kullaniyoruz
    sorgu_kelimeler = sorgu.split()
    if len(sorgu_kelimeler) > 3:
        sorgu = random.choice(sorgu_kelimeler)

    fs = random.sample([inci, eksi, uludag], 3)
    cevap = fs[0](sorgu) or fs[1](sorgu) or fs[2](sorgu)
    cevap_ver(cevap, bot, trigger)


# Kanal gundeminin belirlenmesi
konusulan_kelimeler = []
konusma_sayisi = 0


@module.event('MSG')
@module.rule('.*')
@module.thread(False)
@module.priority('low')
def gundem(bot, trigger):
    # Bunu sadece #ygz icin kullanacagiz
    if (trigger.is_privmsg or trigger.sender != '#ygz'
                           or trigger.nick == bot.nick):
        return None

    # FIXME: globalden baska bir cozum olsa daha iyi olurdu
    global konusulan_kelimeler
    global konusma_sayisi

    for kelime in trigger.split():
        # En az 5 karakterli sadece harf ve rakamlardan
        # olusan kelimeleri ekliyoruz
        if len(kelime) >= 5 and re.match('^\w+$', kelime):
            konusulan_kelimeler.append(kelime.lower())

    konusma_sayisi += 1

    # her 31 mesajlasmada bir, gundem bulunup eksiden cevabi gosteriliyor
    if konusma_sayisi >= 51:
        en_cok_konusulan = Counter(konusulan_kelimeler).most_common(1)[0][0]
        cevap_ver(eksi(en_cok_konusulan), bot, trigger)

        konusulan_kelimeler = []
        konusma_sayisi = 0
