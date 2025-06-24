from telebot import types

btn_raskid = types.KeyboardButton('/создать')
markup = types.ReplyKeyboardMarkup(resize_keyboard = True).add(btn_raskid)