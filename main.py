import re
import json

from collections import Counter

import telebot


with open("token.cfg", "r", encoding="utf-8") as f:
    token = f.read().rstrip()

with open("bazvortaro.json", "r", encoding="utf-8") as f:
    sxava_bazvortaro = json.load(f)
    latina_bazvortaro = {v: s for k, v in sxava_bazvortaro.items()}


with open("reformvortaro.json", "r", encoding="utf-8") as f:
    sxava_reformvortaro = json.load(f)
    latina_reformvortaro = {v: s for k, v in sxava_reformvortaro.items()}


bot = telebot.TeleBot(token)


def divenu_lingvon(teksto):
    mia_kalkulilo = Counter(teksto)
    sxavofto, latinofto = 0, 0
    for k, v in sxava_sercxotablo.items():
        sxavofteco += mia_kalkulilo[k]
        latinofteco += mia_kalkulilo[v]
    diveno = "sxava" if sxavofteco >= latinofteco else "latina"
    return diveno


def traduki(teksto, vortaro):
    for k, v in vortaro.items():
        teksto = re.sub(f"·{k}", v.upper(), teksto)
        teksto = re.sub(k, v, teksto)
    return teksto


def latinigi(teksto):
    teksto = traduki(sxava_reformvortaro)
    teksto = traduki(sxava_bazvortaro)
    return teksto


def sxavigi(teksto):
    teksto = traduki(latina_reformvortaro)
    teksto = traduki(latina_bazvortaro)
    return teksto


@bot.message_handler(content_types="text")
def get_text_messages(message):
    originalo = message.text
    lingvo = divenu_lingvon(originalo)
    match lingvo:
        case "sxava":
            traduko = latinigi(originalo)
        case "latina":
            traduko = sxavigi(originalo)
    teksto = f"<tg-spoiler>{originalo}</tg-spoiler>\n\n{traduko}"
    bot.send_message(message.chat.id, teksto, parse_mode="HTML")


bot.infinity_polling()