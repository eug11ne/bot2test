from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
from json_tools import *
import time


SHARE_PHONE, SHARE_LOC, MAIN_MENU, NEXT_STEPS, SALON, SERVICE, MASTER, ENTER_DATE, TIME_SLOTS, REGISTER, ENTER_CONTACT_INFO, NAME, PAY, ORDERS = range(14)

def share_location(update: Update, context: CallbackContext) -> None:

    chat_id = update.effective_chat.id
    keyboard = [[KeyboardButton('Поделиться расположением', request_location=True)], [KeyboardButton('Нет')]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, row_width=1, resize_keyboard=True)
    context.bot.send_message(chat_id=chat_id, text='Здравствуйте! Этот бот поможет вам записаться на прием в один из наших салонов. Вы можете поделиться своим расположением, чтобы найти ближайший к вам салон.', reply_markup=reply_markup)

    return SHARE_LOC

def get_location(update: Update, context: CallbackContext) -> None:

    if update.message.location is not None:
        context.user_data.update({'location': [update.message.location['longitude'], update.message.location['latitude']]})
        print(context.user_data['location'])
    else:
        context.user_data.update({'location': None})

    kbd = ['Записаться', 'Открыть личный кабинет']
    reply_markup = create_keyboard(kbd)

    update.message.reply_text('Что вы хотели бы сделать?',
                              reply_markup=reply_markup)
    return MAIN_MENU


'''
def start(update: Update, context: CallbackContext) -> None:

    kbd = ['Записаться', 'Открыть личный кабинет']
    reply_markup = create_keyboard(kbd)


    update.message.reply_text('Здравствуйте! Что вы хотели бы сделать?',
                              reply_markup=reply_markup)
    return MAIN_MENU '''

def cancel(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Попробуйте снова с помощью команды /start")
    return ConversationHandler.END




def main_menu(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.answer()
    kbd = ['Записаться', 'Открыть личный кабинет']
    reply_markup = create_keyboard(kbd)
    query.edit_message_text(text='Что вы хотели бы сделать?',
                            reply_markup=reply_markup)
    return MAIN_MENU


''' def share_contacts(update: Update, context: CallbackContext) -> None:
    print('Телефон', update.message.contact)

    return NEXT_STEPS
'''

def main_submenu(update: Update, context: CallbackContext) -> None:

    next_steps = ['Выбрать салон', 'Выбрать услугу', 'Выбрать мастера']
    user_id = update.effective_user.id
    user_name = update.effective_user.username
    print(f'user: {user_name}, {user_id}')
    bot_config = load_json()
    salons = get_salon_names(bot_config)
    services = get_service_names(bot_config)
    all_masters = get_all_master_names(bot_config)

    context.user_data.update({'choose_salon_first': False,
                              'choose_service_first': False,
                              'choose_master_first': False,
                              'reorder': False,
                              'config': bot_config,
                              'salons': salons,
                              'services': services,
                              'all_masters': all_masters})

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

    salons = context.user_data['salons']
    reply_markup = create_keyboard(salons)

    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Выберите подходящий салон:", reply_markup=reply_markup)

    if context.user_data['choose_master_first']:
        return ENTER_DATE
    elif context.user_data['choose_service_first']:
        return MASTER
    else:
        context.user_data.update({'choose_salon_first': True})
        return SERVICE

def choose_service(update: Update, context: CallbackContext) -> None:

    services = context.user_data['services']
    reply_markup = create_keyboard(services)
    print(context.user_data)

    query = update.callback_query
    query.answer()
    if context.user_data['choose_salon_first']:
        current_salon = context.user_data['salons'][int(query.data)]
        context.user_data.update({'salon': current_salon})
        print(context.user_data['salon'])
    query.edit_message_text(text=f"Выберите одну из следующих услуг:", reply_markup=reply_markup)

    if context.user_data['choose_master_first']:
        return SALON
    return MASTER

def choose_master(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.answer()

    if context.user_data['choose_service_first']:
        current_salon = context.user_data['salons'][int(query.data)]
        context.user_data.update({'salon': current_salon})

    masters = get_master_names(context.user_data['config'], context.user_data['salon'])
    reply_markup = create_keyboard(masters)
    print(context.user_data)

    query.edit_message_text(text="Выбранную услугу может оказать один из следующих мастеров:", reply_markup=reply_markup)
    return ENTER_DATE

def choose_date(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Введите подходящую дату в формате ДД.ММ.ГГГГ:")

def enter_date(update, context: CallbackContext) -> None:
    date = update.message.text
    try:
        valid_date = time.strptime(date, '%d.%m.%Y')
    except ValueError:
        update.message.reply_text("Вы ввели неправильную дату. Попробуйте еще раз.")
        return ENTER_DATE

    context.user_data.update({'date': date})
    update.message.reply_text(f'Будем ждать вас {date}')
    slots = ['10:00 - 11:00',
               '11:00 - 12:00',
               '11:00 - 13:00',
               '13:00 - 14:00',
               '14:00 - 15:00',
               ]

    reply_markup = create_keyboard(slots)
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
    chat_id = update.effective_chat.id
    document = open('Agreement.pdf', 'rb')
    pdf_message = context.bot.send_document(chat_id, document, caption='Рекомендуем ознакомиться с соглашением об обработке персональных данных')
    print("message id", pdf_message.message_id)
    context.user_data.update({'pdf_message_id': pdf_message.message_id})
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Нам нужно ваше согласие на обработку персональных данных:", reply_markup=reply_markup)

    return ENTER_CONTACT_INFO


def enter_phone(update, context: CallbackContext) -> None:

    if update.message.contact is not None:
        phone = update.message.contact['phone_number']
    else:
        phone = update.message.text
    context.user_data.update({'phone': phone})
    update.message.reply_text(phone)
    update.message.reply_text("Введите ваше имя:")
    return NAME

def enter_name(update, context: CallbackContext) -> None:
    name = update.message.text
    context.user_data.update({'name': name})
    update.message.reply_text(f"Заказ номер: 1222344\n"
                              f"Имя клиента: {name}\n"
                              f"Номер телефона: {context.user_data['phone']}\n"
                              f"Салон: {context.user_data['salon']}\n"
                              )
    reply_markup = create_keyboard(['Оплатить'])
    update.message.reply_text("Осталось оплатить заказ:", reply_markup=reply_markup)
    return PAY

def process_payment(update, context: CallbackContext) -> None:
    query = update.callback_query
    query.edit_message_text(text="Для оплаты перейдите по ссылке. Скоро она здесь появится")
    return ConversationHandler.END


def choose_contact_info(update, context: CallbackContext) -> None:
    context.bot.delete_message(update.effective_chat.id, context.user_data['pdf_message_id'])
    query = update.callback_query
    keyboard = [[KeyboardButton('Поделиться телефоном', request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, row_width=1, resize_keyboard=True)
    query.answer()
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Введите ваш номер телефона или нажмите кнопку Поделиться телефоном:", reply_markup=reply_markup)

    #query.edit_message_text(text="Введите ваш номер телефона:", reply_markup=reply_markup)


def choose_service_first(update: Update, context: CallbackContext) -> None:

    context.user_data.update({'choose_service_first': True})

    services = context.user_data['services']

    reply_markup = create_keyboard(services)
    print(context.user_data)

    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Выберите одну из следующих услуг, чтобы найти салоны, в которых она предоставляется:", reply_markup=reply_markup)
    return SALON


def choose_master_first(update: Update, context: CallbackContext) -> None:
    context.user_data.update({'choose_master_first': True})
    masters = context.user_data['all_masters']

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
        entry_points=[CommandHandler('start', share_location)],
        states={
            SHARE_LOC: [MessageHandler(Filters.location | Filters.regex('Нет'), get_location)],
            MAIN_MENU: [CallbackQueryHandler(main_submenu, pattern='0'), CallbackQueryHandler(client_area, pattern='1')],
            NEXT_STEPS: [CallbackQueryHandler(choose_salon, pattern='0'), CallbackQueryHandler(choose_service_first, pattern='1'), CallbackQueryHandler(choose_master_first, pattern='2')],
            SALON: [CallbackQueryHandler(choose_salon, pattern='\d+')],
            SERVICE: [CallbackQueryHandler(choose_service, pattern='\d+')],
            MASTER: [CallbackQueryHandler(choose_master, pattern='\d+')],
            ENTER_DATE: [CallbackQueryHandler(choose_date, pattern='\d+'), MessageHandler(Filters.text, enter_date)],
            REGISTER: [CallbackQueryHandler(register_client, pattern='\d+')],
            ENTER_CONTACT_INFO: [MessageHandler(Filters.contact | Filters.text, enter_phone), CallbackQueryHandler(choose_contact_info, pattern='\d+')],
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

