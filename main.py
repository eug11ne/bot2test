from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""

    update.message.reply_text('Please choose:',
                              reply_markup = keyboard_main_menu())


def main_menu(update: Update, context: CallbackContext) -> None:
    """ Displays the main menu keyboard when called. """

    query = update.callback_query
    query.answer()
    query.edit_message_text(text         = 'Please choose:',
                            reply_markup = keyboard_main_menu())


def keyboard_main_menu():
    """ Creates the main menu keyboard """

    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data='1'),
         InlineKeyboardButton("Option 2", callback_data='2'),
         InlineKeyboardButton("Option 3", callback_data='VVV')]
    ]

    return InlineKeyboardMarkup(keyboard)


def confirm(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""

    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton("Yes", callback_data=f'YES{query.data}'),
         InlineKeyboardButton("No",  callback_data='main'),],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(text=f"Selected option {query.data}.\n"
                                 f"Are you sure ? ",
                           reply_markup=reply_markup)
    #query.message.reply_text(text=f"Selected option {query.data}.\n"
    #                             f"Are you sure ? ",
    #                        reply_markup=reply_markup)




def do_action_1(update: Update, context: CallbackContext) -> None:

    keyboard = [[InlineKeyboardButton("Main menu", callback_data='main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Selected option {query.data}\n"
                                 f"Executed action 1.",
                            reply_markup=reply_markup)


def do_action_2(update: Update, context: CallbackContext) -> None:

    keyboard = [[InlineKeyboardButton("Main menu", callback_data='main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Selected option {query.data}\n"
                                 f"Executed action 2.",
                            reply_markup=reply_markup)

def do_action_3(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    clubs = ['Салон в центре', 'Салон слева', 'Салон справа']
    keyboard = [[InlineKeyboardButton(kb, callback_data=kb) for kb in clubs]]
    #for i in range(5):
    query.message.reply_text(text=f"Hello world {query.data}:", reply_markup=InlineKeyboardMarkup(keyboard))

def do456(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    query.message.reply_text(text=f"Hello world {query.data}:")



def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5939603614:AAHQRADVt5SVleCzifGK3nUH1tyJeNfZ104")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    updater.dispatcher.add_handler(CallbackQueryHandler(do_action_3, pattern='VVV'))
    updater.dispatcher.add_handler(CallbackQueryHandler(confirm, pattern='^(|1|2)$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(do_action_1, pattern='YES1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(do_action_2, pattern='YES2'))
    updater.dispatcher.add_handler(CallbackQueryHandler(do456, pattern='(|Салон в центре|Салон слева|Салон справа)'))



    # Start the Bot
    updater.start_polling()
    print('started')

if __name__ == '__main__':
    main()

