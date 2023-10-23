import re
import json

from collections import Counter

import telebot


with open("token.cfg", "r", encoding="utf-8") as f:
    token = f.read().rstrip()


with open("bonvenigo.txt", "r", encoding="utf-8") as f:
    bonvenigo = f.read().rstrip()


with open("bazvortaro.json", "r", encoding="utf-8") as f:
    sxava_bazvortaro = json.load(f)
    latina_bazvortaro = {v: k for k, v in sxava_bazvortaro.items()}
    sxava_bazvortaro_granda = {f"·{k}": v.upper() for k, v in sxava_bazvortaro.items()}
    latina_bazvortaro_granda = {k.upper(): f"·{v}" for k, v in latina_bazvortaro.items()}


with open("reformvortaro.json", "r", encoding="utf-8") as f:
    sxava_reformvortaro = json.load(f)
    latina_reformvortaro = {v: k for k, v in sxava_reformvortaro.items()}
    sxava_reformvortaro_granda = {f"·{k}": v.capitalize() for k, v in sxava_reformvortaro.items()}
    latina_reformvortaro_granda = {k.capitalize(): f"·{v}" for k, v in latina_reformvortaro.items()}


bot = telebot.TeleBot(token)


def divenu_lingvon(teksto):
    mia_kalkulilo = Counter(teksto)
    sxavofto, latinofto = 0, 0
    for k, v in sxava_bazvortaro.items():
        sxavofto += mia_kalkulilo[k]
        latinofto += mia_kalkulilo[v]
    diveno = "sxava" if sxavofto >= latinofto else "latina"
    return diveno


def traduki(teksto, vortaro):
    for k, v in vortaro.items():
        teksto = re.sub(k, v, teksto)
    return teksto


def latinigi(teksto):
    teksto = traduki(teksto, sxava_reformvortaro_granda)
    teksto = traduki(teksto, sxava_bazvortaro_granda)
    teksto = traduki(teksto, sxava_reformvortaro)
    teksto = traduki(teksto, sxava_bazvortaro)
    return teksto


def sxavigi(teksto):
    teksto = traduki(teksto, latina_reformvortaro_granda)
    teksto = traduki(teksto, latina_bazvortaro_granda)
    teksto = traduki(teksto, latina_reformvortaro)
    teksto = traduki(teksto, latina_bazvortaro)
    return teksto


@bot.message_handler(commands=['start'])
def start(message):
    with open(f"bonvenigo.png", "rb") as f:
        bot.send_photo(message.from_user.id, f, caption=bonvenigo)



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
