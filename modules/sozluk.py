""" AT sirk icin sozluk modulu
Orijinal at'a sadik kalinarak rastgele bir sozlukten alinan
entrylerden rastgele bir tanesi gosterimektedir.
"""

import random
import requests
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


def eksi(sorgu):
    r = requests.get('https://eksisozluk.com/', params={'q': sorgu})
    soup = BeautifulSoup(r.text, 'html.parser')
    entry_list = soup.find(id='entry-list')
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


def handler(cevap, bot, trigger):
    if cevap:
        bot.reply(cevap)
    else:
        bot.reply('yok boyle bisi')


@module.commands('eksi')
def eksi_handler(bot, trigger):
    handler(eksi(trigger.group(2)), bot, trigger)


@module.commands('inci')
def inci_handler(bot, trigger):
    handler(inci(trigger.group(2)), bot, trigger)


@module.commands('ulu')
@module.commands('uludag')
def ulu_handler(bot, trigger):
    handler(uludag(trigger.group(2)), bot, trigger)


@module.rule('.+$nickname')
@module.rule('$nickname.+')
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
    if not cevap:
        bot.reply('Hic bisey bulamadim')
    else:
        bot.reply(cevap)
