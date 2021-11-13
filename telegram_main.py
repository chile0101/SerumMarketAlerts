from telegram.ext import Updater, CommandHandler, Dispatcher
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from config import TELE_TOKEN
from raydium import new_pool_alert

updater = Updater(TELE_TOKEN, use_context=True)

dispatcher: Dispatcher = updater.dispatcher


def raydium(update: Update, context: CallbackContext):
    new_pool_alert()


# def dexlab(update: Update, context: CallbackContext):
#     new_pool_alert()


if __name__ == '__main__':
    dispatcher.add_handler(CommandHandler("raydium", raydium))
    # dispatcher.add_handler(CommandHandler("dexlab", dexlab))
    updater.start_polling()
