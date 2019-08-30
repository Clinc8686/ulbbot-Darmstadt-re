# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import telegram


API_TOKEN = 'TOKEN'
bot = telebot.TeleBot(API_TOKEN)

#Navigation
def navigationmessage(message):
    for i in range(message.message_id, (message.message_id-10), -1):
        try:
            bot.delete_message(message.chat.id, i)
        except:
            pass

    bot.send_message(message.chat.id, "Du findest über folgenden Link zu uns: https://goo.gl/maps/Kiypg4WqCotsAYbh7 \nAlternativ ist unsere Adresse: Magdalenenstraße 8, 64289 Darmstadt")
