from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler,CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
import datetime
import os
import urllib
#from urllib.request import urlopen
import json


def start(bot, update):
  print("Inside start")
  kb = [[KeyboardButton('/info')],[KeyboardButton('/exchange')],[KeyboardButton('/euro1')]]
  print("Keyboard created")
  kb_markup = ReplyKeyboardMarkup(kb,resize_keyboard='true')
  print("keyboard loaded")
  bot.send_message(chat_id=update.message.chat_id, text="your message",reply_markup=kb_markup)
  print("end")
  #habria que probar a poner inlinekeyboard
 

def euro1(bot, update):
  print ("un euro")
  update.message.reply_text("un euro")

def info(bot, update, args):
  now = datetime.datetime.now()
  #bot.edit_message_text(text="Selected option: {}".format(query.data), chat_id=query.message.chat_id, message_id=query.message.message_id)
  update.message.reply_text("Hi!!, " + str(now) + str(args))

def exchange(bot,update, args):
  response = urllib.urlopen('http://www.floatrates.com/daily/chf.json')
  data = json.load(response)  
  for key, value in data['eur'].items():
    if key == 'rate':
        vrate = value
    if key == 'date':
        vdate = value

  update.message.reply_text("Rate date: " + str(vdate) + '\n' + "Rate value: " + str(vrate))





def setup():
  # Create Updater object and attach dispatcher to it
  TOKEN = os.environ.get('TELEGRAM_TOKEN')
 
  #print(TOKENV)
  #https://api.telegram.org/file/bot<token>/<file_path>
  updater = Updater(TOKEN)
  dispatcher = updater.dispatcher
  print("Bot started")

  # Add command handler to dispatcher
  start_handler = CommandHandler('start',start)
  dispatcher.add_handler(start_handler)

  info_handler = CommandHandler('info',info, pass_args=True)
  dispatcher.add_handler(info_handler)

  exchange_handler = CommandHandler('exchange',exchange, pass_args=True)
  dispatcher.add_handler(exchange_handler)

  euro1_handler = CommandHandler('euro1',euro1, pass_args=True)
  dispatcher.add_handler(euro1_handler)

  # Start the bot
  updater.start_polling()

  # Run the bot until you press Ctrl-C
  updater.idle()

if __name__ == '__main__':
  setup()