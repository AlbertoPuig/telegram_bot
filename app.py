from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler,CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
import datetime
import os
import requests
import json
from emoji import emojize


def start(bot, update):
  vemoji = 'U+1F4B6'
  kb = [[KeyboardButton('/info' + emojize("  :information:", use_aliases=True))],[KeyboardButton('/exchange' + emojize("  :moneybag:", use_aliases=True))]]
  print("Keyboard created")
  kb_markup = ReplyKeyboardMarkup(kb,resize_keyboard='true')
  print("keyboard loaded")
  bot.send_message(chat_id=update.message.chat_id, text="Please select command or write \n /exchange CHF_value \n or \n /exchange e EUR_value",reply_markup=kb_markup)

def info(bot, update):
  now = datetime.datetime.now()
  update.message.reply_text("Hi!!, " + str(now))

def exchange(bot,update, args):
  vargs = str(args)
  vargs=vargs.replace('u', '')
  vargs=vargs.replace("'", '')
  vargs=vargs.replace("[", '')
  vargs=vargs.replace("]", '')
  try:
    response = requests.get('http://www.floatrates.com/daily/chf.json')
  except:
    response = ''
  data = response.json()
  for key, value in data['eur'].items():
    if key == 'rate':
        vrate = value
    if key == 'date':
        vdate = value
    if key == 'inverseRate':
        vinverseRate = value
  #if args:
  if len(args) == 1 and vargs!='\U0001f4b0': 
    try:
      vvalue=float(vrate)*float(vargs)
    except:
      vvalue="Error"
    update.message.reply_text("Rate date: " + str(vdate) + '\n' + "Rate value: " + str(vrate) + '\n' + str(vargs) + " CHF(Fr) = " + str(vvalue) + " EUR")
  elif len(args) == 2 and args[0] == 'e':
    vargs=vargs.replace('e', '')
    vargs=vargs.replace(',', '')
    vargs=vargs.replace(' ', '')
    try:
      vvalue=float(vinverseRate)*float(vargs)
    except:
      vvalue="Error"
    update.message.reply_text("Rate date: " + str(vdate) + '\n' + "Rate value: " + str(vrate) + '\n' + str(vargs) + " EUR = " + str(vvalue) + " CHF(Fr)")
  else:
    update.message.reply_text("Rate date: " + str(vdate) + '\n' + "1 CHF(Fr) = " + str(vrate) + " EUR")
  
def setup():
  # Create Updater object and attach dispatcher to it
  TOKEN = os.environ.get('TELEGRAM_TOKEN')
  #https://api.telegram.org/file/bot<token>/<file_path>
  updater = Updater(TOKEN)
  dispatcher = updater.dispatcher
  print("Bot started...")

  # Add command handler to dispatcher
  start_handler = CommandHandler('start',start)
  dispatcher.add_handler(start_handler)

  info_handler = CommandHandler('info',info)
  dispatcher.add_handler(info_handler)

  exchange_handler = CommandHandler('exchange',exchange, pass_args=True)
  dispatcher.add_handler(exchange_handler)

  # Start the bot
  updater.start_polling()

  # Run the bot until you press Ctrl-Z
  updater.idle()

if __name__ == '__main__':
  setup()