"""TurEng tabanli basit bir ingilizce-turkce sozluk"""


import requests
from bs4 import BeautifulSoup
from sopel import module


def tureng(kelime):
    r = requests.get('http://tureng.com/en/turkish-english/' +
                     kelime)
    soup = BeautifulSoup(r.text, 'html.parser')
    tablo = soup.find(id='englishResultsTable')
    if not tablo:
        return None

    satirlar = tablo.find_all('tr')

    anlamlar = []

    for satir in satirlar:
        sutunlar = satir.find_all('td')
        if len(sutunlar) < 3:
            continue
        anlamlar.append(sutunlar[3].find('a').get_text().strip())

    return anlamlar


@module.commands('tr')
@module.example('.tr horse')
def translate(bot, trigger):
    """TurEng kullanarak verilen kelimeyi cevirmeye yarar"""
    if not trigger.group(2):
        bot.reply('Neyi cevireyim?')
        return None

    anlamlar = tureng(trigger.group(2))

    if not anlamlar:
        bot.reply('Boyle bisey yok')
    else:
        bot.reply(', '.join(anlamlar))
