#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from random import randint
import requests
import xmltodict

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


PORT = int(os.environ.get('PORT', 8443))

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hola {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


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

def mesa(update: Update, context: CallbackContext) -> None:
    """Sortea el juego de mesa segun bgg collection list"""    
    users = ['maurocor','juankazon','maticepe','juanecasla']
    
    game_list = []
    for user in users:        
        url = "https://www.boardgamegeek.com/xmlapi/collection/{user}?own=1".format(user=user)        
        response = requests.get(url)
        data = xmltodict.parse(response.content)
        for item in data['items']['item']:
            game_list.append({'name': item['name']['#text'], 'thumbnail': item['thumbnail'], 'owner': user})

    game = game_list[randint(0,len(game_list)-1)]    
    caption =  "*{name}*\n{owner}".format(name=game['name'],owner=game['owner'])   
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo = game['thumbnail'] , caption=caption, parse_mode="Markdown")


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    token = os.environ['TOKEN']    
    updater = Updater( token )

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("wz", wz))
    dispatcher.add_handler(CommandHandler("mesa", mesa))

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