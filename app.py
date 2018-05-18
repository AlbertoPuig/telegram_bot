from telegram.ext import Updater, CommandHandler
import datetime
import os

def start(bot, update):
  update.message.reply_text("I'm a bot, Hello")

def info(bot, update):
  now = datetime.datetime.now()
  update.message.reply_text("Hi!!, " + str(now))

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

  info_handler = CommandHandler('info',info)
  dispatcher.add_handler(info_handler)

  # Start the bot
  updater.start_polling()

  # Run the bot until you press Ctrl-C
  updater.idle()

if __name__ == '__main__':
  setup()