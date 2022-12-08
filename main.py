from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ConversationHandler, MessageHandler, Filters


MAIN_MENU, NEXT_STEPS, SALON, SERVICE, MASTER, ENTER_DATE, TIME_SLOTS, REGISTER, ENTER_CONTACT_INFO, NAME, PAY, ORDERS = range(12)


def start(update: Update, context: CallbackContext) -> None:

    kbd = ['Записаться', 'Открыть личный кабинет']
    reply_markup = create_keyboard(kbd)

    update.message.reply_text('Здравствуйте! Что вы хотели бы сделать?',
                              reply_markup=reply_markup)
    return MAIN_MENU

def cancel(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Попробуйте снова с помощью команды /start")
    return ConversationHandler.END


def main_menu(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.answer()
    kbd = ['Записаться', 'Открыть личный кабинет']
    reply_markup = create_keyboard(kbd)
    query.edit_message_text(text         = 'Здравствуйте! Что вы хотели бы сделать?',
                            reply_markup = reply_markup)
    return MAIN_MENU


def main_submenu(update: Update, context: CallbackContext) -> None:
    context.user_data.update({'choose_service_first': False, 'choose_master_first': False, 'reorder': False})

    next_steps = ['Выбрать салон', 'Выбрать услугу', 'Выбрать мастера']

    reply_markup = create_keyboard(next_steps)

    query = update.callback_query
    query.answer()

    query.edit_message_text(text="Вы хотели бы:", reply_markup=reply_markup)
    return NEXT_STEPS



def client_area(update: Update, context: CallbackContext) -> None:
    orders = ['122234', '344224', '333223', '12984']
    reply_markup = create_keyboard(orders)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Вы можете повторить любой из предыдущих заказов:", reply_markup=reply_markup)
    return ORDERS

def choose_order(update: Update, context: CallbackContext) -> None:
    reorder = ['Заказать снова']
    context.user_data.update({'reorder': True})
    reply_markup = create_keyboard(reorder)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Вы заказывали массаж в Салоне на Павелецкой у мастера Ивановой:", reply_markup=reply_markup)
    return ENTER_DATE



def choose_salon(update: Update, context: CallbackContext) -> None:

    salons = ['Салон на Павелецкой',
              'Салон на Пресне',
              'Салон в Сити',
              'Салон на Кутузовском'
              ]

    reply_markup = create_keyboard(salons)

    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Выберите подходящий салон:", reply_markup=reply_markup)

    if context.user_data['choose_master_first']:
        return ENTER_DATE
    elif context.user_data['choose_service_first']:
        return MASTER
    else:
        return SERVICE

def choose_service(update: Update, context: CallbackContext) -> None:

    services = ['Супер-детокс обертывание',
    'Томатное обертывание',
    'Парафинотерапия',
    'Автозагар',
    'Водорослевый пилинг',
    'Парафиновые ванны',
    'Массажная программа']


    reply_markup = create_keyboard(services)
    print(context.user_data)

    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Выберите одну из следующих услуг:", reply_markup=reply_markup)

    if context.user_data['choose_master_first']:
        return SALON
    return MASTER

def choose_master(update: Update, context: CallbackContext) -> None:

    masters = ['Иванова',
    'Сергеева',
    'Цветкова',
    'Капустина']

    reply_markup = create_keyboard(masters)
    print(context.user_data)

    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Выбранную услугу может оказать один из следующих мастеров:", reply_markup=reply_markup)
    return ENTER_DATE

def choose_date(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Введите подходящую дату:")


def enter_date(update, context: CallbackContext) -> None:
    date = update.message.text
    context.user_data.update({'date': date})
    update.message.reply_text(date)
    masters = ['10:00 - 11:00',
               '11:00 - 12:00',
               '11:00 - 13:00',
               '13:00 - 14:00',
               '14:00 - 15:00',
               ]

    reply_markup = create_keyboard(masters)
    update.message.reply_text("Bыберите удобное время:", reply_markup=reply_markup)
    if context.user_data['reorder']:
        return PAY
    else:
        return REGISTER


def register_client(update: Update, context: CallbackContext) -> None:

    registration = ['Я согласен',
                    'Я не согласен'
                    ]

    reply_markup = create_keyboard(registration)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Нам нужно ваше согласие на обработку персональных данных:", reply_markup=reply_markup)
    return ENTER_CONTACT_INFO


def enter_phone(update, context: CallbackContext) -> None:
    phone = update.message.text
    context.user_data.update({'phone': phone})
    update.message.reply_text(phone)
    #reply_markup = create_keyboard(['Оплатить'])
    update.message.reply_text("Введите ваше имя:")
    return NAME

def enter_name(update, context: CallbackContext) -> None:
    name = update.message.text
    context.user_data.update({'name': name})
    update.message.reply_text(f"{name}, номер телефона: {context.user_data['phone']}")
    reply_markup = create_keyboard(['Оплатить'])
    update.message.reply_text("Осталось оплатить заказ:", reply_markup=reply_markup)
    return PAY

def process_payment(update, context: CallbackContext) -> None:
    query = update.callback_query
    query.edit_message_text(text="Для оплаты перейдите по ссылке. Скоро она здесь появится")
    return ConversationHandler.END



def choose_contact_info(update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Введите ваш номер телефона:")


def choose_service_first(update: Update, context: CallbackContext) -> None:

    context.user_data.update({'choose_service_first': True})

    services = [
        'Супер-детокс обертывание',
        'Томатное обертывание',
        'Парафинотерапия',
        'Автозагар',
        'Водорослевый пилинг',
        'Парафиновые ванны',
        'Массажная программа'
                ]

    reply_markup = create_keyboard(services)
    print(context.user_data)

    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Выберите одну из следующих услуг, чтобы найти салоны, в которых она предоставляется:", reply_markup=reply_markup)
    return SALON


def choose_master_first(update: Update, context: CallbackContext) -> None:
    context.user_data.update({'choose_master_first': True})
    masters = [
        'Иванова',
        'Сергеева',
        'Цветкова',
        'Капустина'
        ]


    reply_markup = create_keyboard(masters)
    print(context.user_data)

    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Выберите мастера, к которому вы хотели бы обратиться:", reply_markup=reply_markup)
    return SERVICE

def create_keyboard(button_names):
    keyboard = [[InlineKeyboardButton(kb, callback_data=f'{button_names.index(kb)}')] for kb in button_names]
    return InlineKeyboardMarkup(keyboard)




def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.

    updater = Updater("5939603614:AAHQRADVt5SVleCzifGK3nUH1tyJeNfZ104")

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MAIN_MENU: [CallbackQueryHandler(main_submenu, pattern='0'), CallbackQueryHandler(client_area, pattern='1')],
            NEXT_STEPS: [CallbackQueryHandler(choose_salon, pattern='0'), CallbackQueryHandler(choose_service_first, pattern='1'), CallbackQueryHandler(choose_master_first, pattern='2')],
            SALON: [CallbackQueryHandler(choose_salon, pattern='\d+')],
            SERVICE: [CallbackQueryHandler(choose_service, pattern='\d+')],
            MASTER: [CallbackQueryHandler(choose_master, pattern='\d+')],
            ENTER_DATE: [CallbackQueryHandler(choose_date, pattern='\d+'), MessageHandler(Filters.text, enter_date)],
            REGISTER: [CallbackQueryHandler(register_client, pattern='\d+')],
            ENTER_CONTACT_INFO: [CallbackQueryHandler(choose_contact_info, pattern='\d+'), MessageHandler(Filters.text, enter_phone)],
            NAME: [MessageHandler(Filters.text, enter_name)],
            ORDERS: [CallbackQueryHandler(choose_order, pattern='\d+')],
            PAY: [CallbackQueryHandler(process_payment, pattern='\d+')]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)


    # Start the Bot
    updater.start_polling()
    print('started')

if __name__ == '__main__':
    main()

