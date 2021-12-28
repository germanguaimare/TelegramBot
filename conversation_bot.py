import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

EMOTION, COMMENTARY = range(2)


def start(update: Update, context: CallbackContext) -> int:
    """Inicia la conversación y pregunta el estado de ánimo."""
    reply_keyboard = [['😃', '😐', '😞']]

    update.message.reply_text(
        'Hola, soy un bot diseñado para almacenar tus estados de ánimo '
        'Cuál de estos emojis representa mejor tu estado de ánimo?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Feliz, Regular o Triste?'
        ),
    )

    return EMOTION


def emotion(update: Update, context: CallbackContext) -> int:
    """Almacena la emoción y pide un comentario adicional."""
    user = update.message.from_user
    logger.info("Emoción de %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Ya veo, '
        'Quieres dar un comentario acerca de tu estado de ánimo?',
        reply_markup=ReplyKeyboardRemove(),
    )

    return COMMENTARY

def store(update: Update, context: CallbackContext) -> int:
    """Almacena el comentario y se comunica con la API."""
    user = update.message.from_user
    logger.info("Comentario de %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Gracias por la información' 
        'Almacenaré estos datos.',
    )

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5095765162:AAGmjvUuuef7gWk7Qg57-gt0vogPfCSntH4")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            EMOTION: [MessageHandler(Filters.regex('^(😃|😐|😞)$'), emotion)],
            COMMENTARY: [MessageHandler(Filters.text, store)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()