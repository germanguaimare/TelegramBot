import logging
import requests
import json

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hola, {user.mention_markdown_v2()}, soy un bot creado para enviar tus mensajes a una base de datos\!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Aún no tengo una página de ayuda. Seguimos trabajando para usted.")


def store(update: Update, context: CallbackContext) -> None:
    """Store the user message."""
    message = update.message.text
    url = "https://3001-apricot-scorpion-ulosbcd8.ws-us25.gitpod.io/api/message"

    payload = json.dumps({
        "message": message
        })
    headers = {
        'Content-Type': 'application/json'
        }
    response = requests.request("POST", url, headers=headers, data=payload)
    ## Respuesta del bot:
    update.message.reply_text("Almacené tu mensaje: " + message + ". En la API")

def all_messages(update: Update, context: CallbackContext) -> None:
    """Show all messages to the user message."""
    url = "https://3001-apricot-scorpion-ulosbcd8.ws-us25.gitpod.io/api/message"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    update.message.reply_text(response.text)


    


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5095765162:AAGmjvUuuef7gWk7Qg57-gt0vogPfCSntH4")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("messages", all_messages))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, store))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()