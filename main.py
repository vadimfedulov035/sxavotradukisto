import re
import json

from collections import Counter

import telebot


with open("token.cfg", "r", encoding="utf-8") as f:
    token = f.read().rstrip()

with open("sxava.json", "r", encoding="utf-8") as f:
    sxava_sercxotablo = json.load(f)
    latina_sercxotablo = {v: s for s, v in sxava_sercxotablo.items()}


bot = telebot.TeleBot(token)


def sxava_al_latina(teksto):
    for sxlosilo, varo in sxava_sercxotablo.items():
        teksto = re.sub(f"·{sxlosilo}", varo.upper(), teksto)
        teksto = re.sub(sxlosilo, varo, teksto)
    return teksto


def latina_al_sxava(teksto):
    for sxlosilo, varo in latina_sercxotablo.items():
        teksto = re.sub(sxlosilo.upper(), f"·{varo}", teksto)
        teksto = re.sub(sxlosilo, varo, teksto)
    return teksto


def divenu_lingvon(teksto):
    mia_kalkulilo = Counter(teksto)
    sxavofteco, latinofteco = 0, 0
    for sxlosilo, varo in sxava_sercxotablo.items():
        sxavofteco += mia_kalkulilo[sxlosilo]
        latinofteco += mia_kalkulilo[varo]
    diveno = "sxava" if sxavofteco >= latinofteco else "latina"
    return diveno


@bot.message_handler(content_types="text")
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


bot.infinity_polling()
