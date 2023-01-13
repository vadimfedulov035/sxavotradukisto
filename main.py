import re
import requests
import json
import time

from collections import Counter

import telebot


with open("token.cfg", "r", encoding="utf-8") as f:
    token = f.read().rstrip()

with open("sxava.json", "r", encoding="utf-8") as f:
    sxava_sercxotablo = json.load(f)
    latina_sercxotablo = {v: s for s, v in sxava_sercxotablo.items()}


bot = telebot.TeleBot(token)


def sxava_al_latina(teksto):
    for sxlosilo, variablo in sxava_sercxotablo.items():
        teksto = re.sub(f"·{sxlosilo}", variablo.upper(), teksto)
        teksto = re.sub(sxlosilo, variablo, teksto)
    return teksto


def latina_al_sxava(teksto):
    for sxlosilo, variablo in latina_sercxotablo.items():
        teksto = re.sub(sxlosilo.upper(), f"·{variablo}", teksto)
        teksto = re.sub(sxlosilo, variablo, teksto)
    return teksto


def divenu_lingvon(teksto):
    mia_kalkulilo = Counter(teksto)
    sxavajx_nombro, latinajx_nombro = 0, 0
    for sxlosilo, variablo in sxava_sercxotablo.items():
        sxavajx_nombro += mia_kalkulilo[sxlosilo]
        latinajx_nombro += mia_kalkulilo[variablo]
    diveno = "sxava" if sxavajx_nombro >= latinajx_nombro else "latina"
    return diveno


@bot.message_handler(func=lambda m: True)
def get_text_messages(message):
    originalo = message.text
    lingvo = divenu_lingvon(originalo)
    match lingvo:
        case "sxava":
            traduko = sxava_al_latina(originalo)
        case "latina":
            traduko = latina_al_sxava(originalo)
    teksto = f"<tg-spoiler>{originalo}</tg-spoiler>\n\n{traduko}"
    bot.send_message(message.chat.id, teksto, parse_mode="HTML")


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as exc:
        print(exc)
        time.sleep(15)
