# -*- coding: utf-8 -*-

import time
import random
from sopel import module


def rastgele_bi_yer_bul(bot, trigger):
    mekanlar = ['Öğretmenevi', 'Hacıbaba', 'Özgüngör Kebapcı',
                'Hamburger', 'Cici']
    bot.say('Dünyanın konumu hesaplaniyor...')
    time.sleep(2)
    bot.say('1000. asal sayı dünyanın konumundan çıkarılıyor...')
    time.sleep(3)
    bot.say('Gezegenlerin konumundan bugun tercih edilebilecek yer: ' +
            random.choice(mekanlar))


def zaman_hesapla(bot, trigger):
    t = time.time() + 780
    bot.say(time.strftime("%H:%M", time.localtime(t)) + ' go')


@module.commands('yemek')
@module.commands('y')
def yemek(bot, trigger):
    if not trigger.group(2):
        rastgele_bi_yer_bul(bot, trigger)
    elif trigger.group(2) == 'go':
        zaman_hesapla(bot, trigger)
