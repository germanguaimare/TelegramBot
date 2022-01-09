# This example show how to use inline keyboards and process button presses
import telebot
from datetime import datetime
import json, requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


bot = telebot.TeleBot("5063497991:AAEX_bLGzoIzyPkC2gWBU7kZsjIvuvM2Pds")

username = ""
global comment
comment = ""

def ask_comment(call, emotion):

    return bot.send_message(call.message.json['chat']['id'], "¿Quieres agregar un comentario a tu estado de ánimo?",reply_markup=comment_keyboard())

## Post a la API:
def upload_info(username, emotion, comment, fecha):
    url = "https://3001-rose-haddock-94adoe3x.ws-us25.gitpod.io/api/bot"
    payload = json.dumps({
        ##"username": update["message"]["chat"]["username"],
        "username": username,
        "respuesta": emotion,
        "fecha": fecha,
        "comentario": comment
    })
    headers = {
            'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print("Intenté agregar información a la API")

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("😃", callback_data="cb_feliz"),
                InlineKeyboardButton("😐", callback_data="cb_regular"),
                InlineKeyboardButton("😞", callback_data="cb_triste"))
    return markup

def comment_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Sí", callback_data="cb_comment"),
                InlineKeyboardButton("No", callback_data="cb_no_comment"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    username = call.message.json['chat']['username']
    global fecha
    fecha = str(datetime.fromtimestamp(call.message.date))
    global emotion
    if call.data == "cb_feliz":
        emotion = "😃"  
        ask_comment(call, emotion)  
    elif call.data == "cb_regular":
        emotion = "😐"
        ask_comment(call, emotion)
    elif call.data == "cb_triste":
        emotion = "😞"
        ask_comment(call, emotion)
    if call.data == "cb_comment":
        bot.send_message(call.message.json['chat']['id'], "Bien, ¿qué me quieres comentar?") 
        @bot.message_handler(func=lambda message: message.text != '/start')
        def add_comment(message):
            comment = message.text
            bot.send_message(message.chat.id, "Muchas gracias. Almacenaré tu estado de ánimo y comentario en mi base de datos.")
            upload_info(username, emotion, comment, fecha)
    elif call.data == "cb_no_comment":
        bot.send_message(call.message.json['chat']['id'], "De acuerdo. Agregaré tu estado de ánimo sin comentarios adicionales en mi base de datos.")
        upload_info(username, emotion, comment, fecha)

@bot.message_handler(func=lambda message: True, commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id, "Hola, me llamo Ánibot. Soy un bot creado para registrar tus estados de ánimo.")
    bot.send_message(message.chat.id, "Por favor, de estos tres emojis escoge el que mejor represente tu estado de ánimo", reply_markup=gen_markup())


bot.infinity_polling()