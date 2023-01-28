import re
import requests
import json
import time

from collections import Counter

import telebot
import numpy as np


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


def dekuma_al_sesuma(teksto):
    deknombroj = re.findall(r"\d+", teksto)
    sesnombroj = []
    for deknombro in deknombroj:
        sesnombro = np.base_repr(int(deknombro), base=6)
        sesnombroj.append(sesnombro)
    for deknombro, sesnombro in zip(deknombroj, sesnombroj):
        teksto = re.sub(deknombro, sesnombro, teksto)
    return teksto


def sesuma_al_dekuma(teksto):
    sesnombroj = re.findall(r"\d+", teksto)
    deknombroj = []
    for sesnombro in sesnombroj:
        deknombro = int(str(sesnombro), 6)
        deknombroj.append(deknombro)
    for sesnombro, deknombro in zip(deknombroj, sesnombroj):
        teksto = re.sub(sesnombro, deknombro, teksto)
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
            traduko = sesuma_al_dekuma(traduko)
        case "latina":
            traduko = latina_al_sxava(originalo)
            traduko = dekuma_al_sesuma(traduko)
    teksto = f"<tg-spoiler>{originalo}</tg-spoiler>\n\n{traduko}"
    bot.send_message(message.chat.id, teksto, parse_mode="HTML")


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as exc:
        print(exc)
        time.sleep(15)
