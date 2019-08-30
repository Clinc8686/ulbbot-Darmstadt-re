# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import telegram

API_TOKEN = 'TOKEN'
bot = telebot.TeleBot(API_TOKEN)
call = None

#Delete all messages
def botdelete(message, decisionclear):
    if decisionclear == "yes":
        bot.send_message(message.chat.id, "Löschvorgang begonnen. Bitte warte bis alle Nachrichten gelöscht wurden oder ich dir eine neue Nachricht zur Beendigung des Vorgangs sende!⏳")
        for i in range(message.message_id, 0, -1):
            try:
                bot.delete_message(message.chat.id, i)
            except:
                pass
        bot.delete_message(message.chat.id, message.message_id+1)
        bot.send_message(message.chat.id, "Alle Nachrichten wurden gelöscht ✔")
    else:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Löschvorgang abgebrochen ❌")

#Delete start
def clear(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Ja, alles löschen", callback_data="yesdelete"))
    markup.add(InlineKeyboardButton("Nein, nicht löschen", callback_data="notdelete"))
    bot.send_message(message.chat.id, "Das löschen aller Nachrichten kann einige Zeit dauern (bis zu 1. Minute). Möchtest du trotzdem fortfahren?", reply_markup=markup)
