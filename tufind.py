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
call = None

def SearchResult(url, message):
    #List searchresult and selection
    html = urlopen(url).read()
    soup = str(BeautifulSoup(html, 'lxml'))
    global result
    result = re.findall('<div class=\"result recordId\" id=\"record(.+?)\">',soup)
    name = re.findall('(?:<a class=\"link grey-link\" data-ajax=\"false\".+?)\">\n(.+?\n.+?)<\/a>\n<br\/>',soup)

    global forward, backward
    if 'title="next page">weiter »</a>' in soup:
        forward = True
    else:
        forward = False

    if 'title="previous page">« zurück</a>' in soup:
        backward = True
    else:
        backward = False
    if call != None:
        message = call.message

    KeyboardResult(name, message)

#Searchresut & forward/backward button
def KeyboardResult(name, message):
    markup = InlineKeyboardMarkup()
    x = 0
    y = 1
    for i in name:
        i = i.replace("\n","").replace("  ","")
        markup.add(InlineKeyboardButton(str(str(y) + ": " + i), callback_data=result[x]))
        x+=1
        y+=1
    if forward == True:
        markup.add(InlineKeyboardButton("Weiter ⏩ ", callback_data="forward"))
    if backward == True:
        markup.add(InlineKeyboardButton("Zurück ⏪ ", callback_data="backward"))
    bot.send_message(message.chat.id, "Bitte wähle ein Ergebnis aus", reply_markup=markup)

#Edit/filter choosed result 
def ChoosedSearch(link, call):
    #open choosed result
    link = 'https://hds.hebis.de/ulbda/Record/' + link
    htmlsite = urlopen(link).read()
    soupsite = str(BeautifulSoup(htmlsite, 'lxml'))

    #Filter out informations
    name = re.findall('fulltitle">(.+?)<!--', soupsite)
    author = re.findall('author&amp;lastposition\">(.+?)</a>', soupsite)
    released = re.findall('<th>Veröffentlicht:</th>\n<td>\n(.+?)</td>', soupsite)
    media = re.findall('<th>Format:<\/th>\n<td>\n<span class=\"iconlabel book\">(.+?)</span>', soupsite)

    #find link  to copy data
    SignatureLink = re.findall('<a\shref=\"(.+?)\">Exemplare<\/a>', soupsite)
    SignatureLink[0] = SignatureLink[0].replace("[","").replace("]","").replace("'","")
    htmlsitesecond = urlopen(SignatureLink[0]).read()
    soupsitesecond = str(BeautifulSoup(htmlsitesecond, 'lxml'))

    #find booking signing & location
    signatur = re.findall('<th>Signatur: <\/th>\n<td>(.+?)\n', soupsitesecond)
    location = re.findall('<br\/>(.+?)\n\s', soupsitesecond)
    status = re.findall('<span class=\"available\">(.+?)<\/span>', soupsitesecond)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Zurück zu den Suchergebnissen ↩ ", callback_data="search"))
    markup.add(InlineKeyboardButton("Neue Suche starten 🆕 🔎", callback_data="newsearch"))

    if name[0]:
        info = str("*Vollständiger Name:* " + name[0].replace("</a>","") + "\n")
        try:
            info = str(info + ("*Medium:* " + media[0]))
            if media[0] == "Buch":
                info = str(info + " 📕" + "\n")
            elif media[0] == "Ebook":
                info = str(info + " 📲" + "\n")
            elif media[0] == "Artikel":
                info = str(info + " 📄" + "\n")
            elif media[0] == "Zeitschrift, Zeitung":
                info = str(info + " 📰" + "\n")
            elif media[0] == "Schriftenreihe, Mehrbändiges Werk":
                info = str(info + " 📚" + "\n")
            elif media[0] == "Noten":
                info = str(info + " 🎶" + "\n")
            elif media[0] == "Karte":
                info = str(info + " 🗺" + "\n")
            else:
                info = str(info + "\n")
        except:
            pass
        try:
            info = str(info + ("📝 *Autor:* " + author[0] + "\n"))
        except:
            pass
        try:
            info = str(info + ("📢 *Veröffentlicht:* " + released[0].replace("  ","").replace("<br/>","") + "\n"))
        except:
            pass
        try:
            info = str(info + ("📍 *Standort:* " + location[0] + "\n"))
        except:
            pass
        try:
            info = str(info + ("🔖 *Signatur:* " + signatur[0] + "\n"))
        except:
            pass
        try:
            if status[0] == "verfügbar":
                info = str(info + ("*Status:* ✔" + status[0] + "\n"))
            elif status[0] == "ausgeliehen":
                 info = str(info + ("*Status:* ❌" + status[0] + "\n"))
            elif status[0] == "nur vor Ort benutzbar":
                 info = str(info + ("*Status:* ☑" + status[0] + "\n"))
        except:
            pass
        bot.send_message(call.message.chat.id, str(info), parse_mode= 'Markdown', reply_markup=markup)

#Start search query on website
def openpage(call, site, searchitem):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id, "%s Seite wird geöffnet..." % site)
    SearchResult("https://hds.hebis.de/ulbda/Search/Results?lookfor=" + searchitem.replace(" ","+")+"&type=allfields&filters=on&view=list&page=" + str(site), call.message)

