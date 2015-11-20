
from sopel import module
import time


@module.commands('sarap')
@module.commands('s')
@module.thread(False)
def sarap(bot, trigger):
    # sarabi koydugumuz tarih
    sarap = time.mktime(time.strptime('20 Nov 2015', '%d %b %Y'))
    delta = time.time() - sarap

    # deltayi gune cevirelim
    gun = int(round(delta / (60 * 60 * 24)))

    bot.reply('Sarap gun sayisi: ' + str(gun))
