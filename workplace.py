# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

API_TOKEN = 'TOKEN'
bot = telebot.TeleBot(API_TOKEN)

#Open website to the seats
html = urlopen('https://www.ulb.tu-darmstadt.de/service/lernort_bibliothek/freie_arbeitsplaetze/diagramme/index.de.jsp').read()
soup = str(BeautifulSoup(html, 'lxml'))
floor = re.findall('<h3>(.+?)<\/h3><p>Plätze gesamt:', soup) #which floor?
secondhtml = re.findall('<param name="src" value="(.+?)"\/>', soup) #Find url to the seats

def seats(message):
    for i in range(message.message_id, (message.message_id-10), -1):
        try:
            bot.delete_message(message.chat.id, i-1)
        except:
            pass

    try:
        seatsfree = [0,1,2,3,4,5,6]
        seatsoccupied = [0,1,2,3,4,5,6]
        x = 0
        for i in secondhtml:
            htmltemp = urlopen(i).read()
            htmltemp = str(BeautifulSoup(htmltemp, 'lxml'))
            seattempfree = re.search('summary=\"Ungefähr (.+?) Plätze sind frei. Ungefähr', htmltemp)
            seatsfree[x] = seattempfree[1]
            seattempoccupied = re.search(' Plätze sind frei. Ungefähr (.+?) Plätze sind belegt.\">',htmltemp)
            seatsoccupied[x] = seattempoccupied[1]

            if x == 0:
                outputseats = "🏙 Stadtmitte: \n"
                outputseats = str(outputseats + floor[x] + ": \n🆓 " + seatsfree[x] + " frei. ⛔ " + seatsoccupied[x] + " belegt.\n\n")
            elif x == 4:
                outputseats = outputseats + "🏢 Lichtwiese: \n"
                outputseats = str(outputseats + floor[x] + ": \n🆓 " + seatsfree[x] + " frei. ⛔ " + seatsoccupied[x] + " belegt.\n\n")
            else:
                outputseats = str(outputseats + floor[x] + ": \n🆓 " + seatsfree[x] + " frei. ⛔ " + seatsoccupied[x] + " belegt.\n\n")
            x+=1
    except:
        outputseats = "Ich habe keine Infos für dich, da wir geschlossen haben. 🕗"

    bot.send_message(message.chat.id, outputseats)
