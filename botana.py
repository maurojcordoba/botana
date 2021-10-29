#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

import logging
import os, json, promiedos
from telegram import Update, ForceReply, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from random import randint

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

INPUT_TEXT = 0

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hola {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def echo(update: Update, context: CallbackContext) -> None:
    if(update.message.text.startswith('/')):
        """Echo the user message."""
        with open('frases.txt',encoding="utf-8") as f:
            lines = [line.rstrip() for line in f]    
        frase = lines[randint(0,len(lines)-1)]
                
        update.message.reply_text(frase)

def wz(update: Update, context: CallbackContext) -> None:
    """Wz señal"""    
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo = open('images/wz.jpg','rb'), parse_mode="Markdown")

def saluda_command_handler(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Dime tu nombre:')
    return INPUT_TEXT

def input_text(update: Update, context: CallbackContext) -> int:
    text = update.message.text

    chat = update.message.chat
    chat.send_action(
        action=ChatAction.TYPING,
        timeout=None

    )

    saludo = 'Hola {0}!!!!'.format(text)

    update.message.reply_text(saludo)

    return ConversationHandler.END

def partidos_hoy(update: Update, context: CallbackContext) -> None:
    ligas_json = os.getenv('LIGAS')
    ligas = json.loads(ligas_json)["ligas"]

    texto = promiedos.partidos_hoy(ligas)

    update.message.reply_text(texto, parse_mode='Markdown')

def partidos_aye(update: Update, context: CallbackContext) -> None:
    ligas_json = os.getenv('LIGAS')
    ligas = json.loads(ligas_json)["ligas"]

    texto = promiedos.partidos_ayer(ligas)

    update.message.reply_text(texto, parse_mode='Markdown')

def partidos_man(update: Update, context: CallbackContext) -> None:
    ligas_json = os.getenv('LIGAS')
    ligas = json.loads(ligas_json)["ligas"]

    texto = promiedos.partidos_man(ligas)

    update.message.reply_text(texto, parse_mode='Markdown')    

def main() -> None:
    """Start the bot."""

    # Create the Updater and pass it your bot's token.    
    token = os.environ['TOKEN']    
    
    updater = Updater( token )

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))    
    dispatcher.add_handler(CommandHandler("wz", wz))
    dispatcher.add_handler(CommandHandler("hoy", partidos_hoy))
    dispatcher.add_handler(CommandHandler("man", partidos_man))
    dispatcher.add_handler(CommandHandler("aye", partidos_aye))
    

    dispatcher.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('saluda', saluda_command_handler)
        ],

        states={
            INPUT_TEXT: [MessageHandler(Filters.text, callback=input_text)]
        },

        fallbacks=[]
    ))

    # on non command i.e message - echo the message on Telegram
    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot
    updater.start_polling()
 
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()