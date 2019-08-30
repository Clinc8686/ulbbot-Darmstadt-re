# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import telegram

API_TOKEN = 'TOKEN'
bot = telebot.TeleBot(API_TOKEN)

#opening hours
def opening(message):
    for i in range(message.message_id, (message.message_id-10), -1):
        try:
            bot.delete_message(message.chat.id, i)
        except:
            pass

    bot.send_message(message.chat.id, "Generelle Öffnungszeiten Stadtmitte: \n🏔Januar bis März: täglich 24 Stunden offen \n🌄April bis Mai: täglich von 08:00 - 01:00 offen \n🌅Juni bis August: täglich 24 Stunden offen \n⛰September bis Dezember: täglich von 08:00 - 01:00 offen \n\nGenerelle Öffnungszeiten Lichtwiese: \n•Mo - Fr: 08:00 - 22:00 Uhr \n•Sa:         10:00 - 20:00")
