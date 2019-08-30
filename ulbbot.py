# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import telegram

import navigation
import helpmessage
import tufind
import workplace
import clearmessages
import open

API_TOKEN = 'TOKEN'
bot = telebot.TeleBot(API_TOKEN)
call = None

#Start search
@bot.message_handler(commands=['search'])
def search(message):
    for i in range(message.message_id, (message.message_id-10), -1):
        try:
            bot.delete_message(message.chat.id, i-1)
        except:
            pass

    try:
        global searchitem
        searchitem = re.findall('(?<=search\s)(.*)', message.text)
        bot.send_message(message.chat.id, "Ich suche nach dem Buch \"%s\". Bitte einen kurzen Moment warten. 🔎" % searchitem[0])
        tufind.SearchResult("https://hds.hebis.de/ulbda/Search/Results?lookfor=" + searchitem[0].replace(" ","+") + "&trackSearchEvent=Einfache+Suche&type=allfields&search=new&submit=Suchen", message)
        global site
        site=1
    except:
        bot.send_message(message.chat.id, "Bitte gib einen möglichen Suchbegriff ein, der auch keine Sonderzeichen beinhaltet. 🙄")

#delete start
@bot.message_handler(commands=['clear'])
def clear(message):
     clearmessages.clear(message)

#Evaluation of the inline keyboard buttons
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global site
    try:
        site
    except:
        site = 2

    if call.data == "forward":
        site+=1
        tufind.openpage(call, site, searchitem[0])
    elif call.data == "backward":
        site-=1
        tufind.openpage(call, site, searchitem[0])
    elif call.data == "newsearch":
        bot.send_message(call.message.chat.id, "Um eine neue Suche zu starten, gib einfach deinen Suchbegriff hinter \"/search\" ein")
    elif call.data == "search":
        tufind.openpage(call, site, searchitem[0])
    elif call.data == "yesdelete":
        clearmessages.botdelete(call.message, "yes")
    elif call.data == "notdelete":
        clearmessages.botdelete(call.message, "no")
    else:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id, "Ergebnis wird geöffnet... 📂")
        tufind.ChoosedSearch(call.data, call)

#Help command
@bot.message_handler(commands=['help','start'])
def help(message):
    helpmessage.help(message)

#Seating
@bot.message_handler(commands=['freeseats', 'seats'])
def seats(message):
    workplace.seats(message)

#Navigation
@bot.message_handler(commands=['navi', 'navigation'])
def navi(message):
    navigation.navigationmessage(message)

#Opening hours
@bot.message_handler(commands=['opening', 'open'])
def opening(message):
    open.opening(message)

bot.infinity_polling(True)

while True:
    pass
