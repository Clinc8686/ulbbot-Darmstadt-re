# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import telegram

API_TOKEN = 'TOKEN'
bot = telebot.TeleBot(API_TOKEN)
commands = {
    'help'      : '🆘 Was kann ich eigentlich?',
    'search'    : '🔎 Durchsuche die Bibliothek nach dem Medium, das dahinter geschrieben wird. Beispiel: \"/search hessen\"',
    'clear'     : '💥 Lösche alle Nachrichten in diesem Chat',
    'seats'     : '🆓 Freie Sitzplätze in der ULB Darmstadt?',
    'navigation': '🧭 Wie kommst du wohl am schnellsten zur ULB?', #Lichtwiese Abfrage
    'opening'   : '📆 Wann komme ich in die ULB?'
}

#Help command
def help(message):
    for i in range(message.message_id, (message.message_id-10), -1):
        try:
            bot.delete_message(message.chat.id, i)
        except:
            pass

    help_text = "Die folgenden Kommandos können ausgeführt werden: \n"
    for name in commands:
        help_text += "/" + name + ": "
        help_text += commands[name] + "\n"
    bot.send_message(message.chat.id, help_text)
