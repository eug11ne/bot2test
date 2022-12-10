from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardMarkup, LabeledPrice
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ConversationHandler, MessageHandler, Filters, PreCheckoutQueryHandler
from json_tools import *
import time
from geopy.distance import geodesic
import numpy as np
from datetime import timedelta, datetime
import os


SHARE_LOC_REQUEST, SHARE_LOC, MAIN_MENU, NEXT_STEPS, SALON, SERVICE, SERVICE_GEO, MASTER, ENTER_DATE, TIME_SLOTS, REGISTER, ENTER_CONTACT_INFO, NAME, PAY, ORDERS = range(15)

SBER_TOKEN = '401643678:TEST:dafbe70b-9c49-4b23-b0b0-92527a1a21dd'
USERS_JSON = 'users_struct.json'

with open(USERS_JSON, 'r', encoding='utf-8') as file_users:
    if os.stat(USERS_JSON).st_size:
        USERS = json.load(file_users)
    else:
        USERS = {}

def share_location(update: Update, context: CallbackContext) -> None:

    user_id = update.effective_user.id
    user_name = update.effective_user.username
    print(f'user: {user_name}, {user_id}')
    bot_config = load_json('config.json')


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

    chat_id = update.effective_chat.id
    keyboard = [[KeyboardButton('Да', request_location=True)], [KeyboardButton('Нет')]]
    reply_markup = ReplyKeyboardMarkup(keyboard, row_width=1, one_time_keyboard=True, resize_keyboard=True)
    context.bot.send_message(chat_id=chat_id, text='Если хотите выбрать ближайший салон, нажмите кнопку Да. В противном случае нажмите кнопку Нет.', reply_markup=reply_markup)

    return SHARE_LOC

def get_location(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.username
    print(f'user: {user_name}, {user_id}')
    bot_config = load_json('config.json')
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
                              'all_masters': all_masters,
                              'salon': None,
                              'service': None,
                              'master': None})

    if update.message.location is not None:
        yes_no = ['Да', 'Нет']
        context.user_data.update({'location': [update.message.location['latitude'], update.message.location['longitude']]})
        print(context.user_data['location'])
        closest_salon = find_closest_salon(context.user_data['config'], context.user_data['salons'], context.user_data['location'])
        reply_markup = create_keyboard(yes_no)
        context.bot.send_message(chat_id=chat_id, text=f"Ближе всего к вам находится {closest_salon}. Выбрать его?", reply_markup=reply_markup)
        context.user_data.update({'salon': closest_salon})
        context.user_data.update({'choose_salon_first': True})
        return SERVICE_GEO

    else:
        context.user_data.update({'location': None})

    next_steps = ['Выбрать салон', 'Выбрать услугу', 'Выбрать мастера']
    '''
    user_id = update.effective_user.id
    user_name = update.effective_user.username
    print(f'user: {user_name}, {user_id}')
    bot_config = load_json('config.json')    
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
'''
    reply_markup = create_keyboard(next_steps)

    #query = update.callback_query
    #query.answer()


    context.bot.send_message(chat_id=chat_id, text="Вы хотели бы:", reply_markup=reply_markup)
    return NEXT_STEPS

def start(update: Update, context: CallbackContext) -> None:

    kbd = ['Записаться', 'Открыть личный кабинет']
    reply_markup = create_keyboard(kbd)

    bot_config = load_json('config.json')
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

    update.message.reply_text('Здравствуйте! Что вы хотели бы сделать?',
                              reply_markup=reply_markup)
    return SHARE_LOC_REQUEST

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


def main_submenu(update: Update, context: CallbackContext) -> None:

    next_steps = ['Выбрать салон', 'Выбрать услугу', 'Выбрать мастера']
    user_id = update.effective_user.id
    user_name = update.effective_user.username
    print(f'user: {user_name}, {user_id}')

    reply_markup = create_keyboard(next_steps)

    query = update.callback_query
    query.answer()

    query.edit_message_text(text="Вы хотели бы:", reply_markup=reply_markup)
    return NEXT_STEPS

def client_area(update: Update, context: CallbackContext) -> None:
    user_id = str(update.effective_user.id)

    if user_id in USERS:
        message_text = f'Вы зарегистрированы как: {USERS[user_id]["name"]}\n' \
                       f'Номер телефона: {USERS[user_id]["phone"]}'
    else:
        message_text = f'К сожалению вы не зарегистрированы в нашей системе'

    user_name = update.effective_user.username
    bot_users = load_json('USERS.json')
    orders = get_orders(bot_users, user_name)
    context.user_data.update({'orders': orders})
    context.user_data.update({'user_name': user_name})
    context.user_data.update({'users': bot_users})
    reply_markup = create_keyboard(orders)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=message_text, reply_markup=reply_markup)
    return ORDERS

def choose_order(update: Update, context: CallbackContext) -> None:
    reorder = ['Заказать снова']
    context.user_data.update({'reorder': True})
    reply_markup = create_keyboard(reorder)
    query = update.callback_query
    query.answer()
    order_details = get_order_details(context.user_data['users'], context.user_data['user_name'], context.user_data['orders'][int(query.data)])

    query.edit_message_text(text=f"Заказ {context.user_data['orders'][int(query.data)]}\n"
                                 f"Услуга: {order_details['service']}\n"
                                 f"Салон: {order_details['salon']}\n"
                                 f"Мастер: {order_details['master']}", reply_markup=reply_markup)
    context.user_data.update({'service': order_details['service']})
    context.user_data.update({'salon': order_details['salon']})
    context.user_data.update({'master': order_details['master']})
    return ENTER_DATE

def choose_salon(update: Update, context: CallbackContext) -> None:

    salons = context.user_data['salons']
    reply_markup = create_keyboard(salons)

    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Выберите подходящий салон.", reply_markup=reply_markup)

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
    if context.user_data['choose_salon_first'] and context.user_data['salon'] is None:
        current_salon = context.user_data['salons'][int(query.data)]
        context.user_data.update({'salon': current_salon})
        print(context.user_data['salon'])
    query.edit_message_text(text=f"Выберите одну из следующих услуг:", reply_markup=reply_markup)

    if context.user_data['choose_master_first']:
        current_master = context.user_data['all_masters'][int(query.data)]
        context.user_data.update({'master': current_master})
        return SALON
    return MASTER

def choose_master(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.answer()

    if context.user_data['choose_service_first']:
        current_salon = context.user_data['salons'][int(query.data)]
        context.user_data.update({'salon': current_salon})

    available_masters = get_master_names(context.user_data['config'], context.user_data['salon'])
    context.user_data.update({'masters': available_masters})
    reply_markup = create_keyboard(available_masters)
    print(context.user_data)

    query.edit_message_text(text="Выбранную услугу может оказать один из следующих мастеров:", reply_markup=reply_markup)
    return ENTER_DATE

def choose_date(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    if context.user_data['choose_salon_first']:
        current_master = context.user_data['masters'][int(query.data)]
        context.user_data.update({'master': current_master})
    if context.user_data['choose_master_first']:
        current_salon = context.user_data['salons'][int(query.data)]
        context.user_data.update({'salon': current_salon})

    query.answer()
    query.edit_message_text(text="Введите подходящую дату в формате ДД.ММ.ГГГГ:")

def enter_date(update, context: CallbackContext) -> None:
    date = update.message.text
    try:
        valid_date = datetime.strptime(date, '%d.%m.%Y')
    except ValueError:
        update.message.reply_text("Вы ввели неправильную дату. Попробуйте еще раз.")
        return ENTER_DATE
    if valid_date < datetime.now():
        update.message.reply_text("Вы ввели дату в прошлом. Попробуйте еще раз.")
        return ENTER_DATE
    elif (valid_date - datetime.now()).days > 30:
        update.message.reply_text("Мы не принимаем заказы более чем на месяц вперед. Попробуйте еще раз.")
        return ENTER_DATE

    context.user_data.update({'date': date})

    update.message.reply_text(f'Будем ждать вас {date}')
    slots = ['10:00 - 11:00',
               '11:00 - 12:00',
               '12:00 - 13:00',
               '13:00 - 14:00',
               '14:00 - 15:00',
               ]

    reply_markup = create_keyboard(slots)
    context.user_data.update({'slots': slots})
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
    chosen_slot = context.user_data['slots'][int(query.data)]
    context.user_data.update({'slot': chosen_slot})
    query.edit_message_text(text="Нам нужно ваше согласие на обработку персональных данных. Ознакомьтесь с нашей Политикой Конфиденциальности: https://dvmn.org/policy/", reply_markup=reply_markup)

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
    update.message.reply_text(f"Номер заказа: 1222344\n"
                              f"Имя клиента: {name}\n"
                              f"Номер телефона: {context.user_data['phone']}\n"
                              f"Дата: {context.user_data['date']}\n"
                              f"Время: {context.user_data['slot']}\n"
                              f"Салон: {context.user_data['salon']}\n"
                              f"Мастер: {context.user_data['master']}"
                              )

    user_id = str(update.effective_user.id)

    if user_id not in USERS:
        USERS[user_id] = {
            'name': name,
            'phone': context.user_data['phone'],
            'orders': []
        }

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Оплатить', callback_data=0)]])
    update.message.reply_text("Осталось оплатить заказ:", reply_markup=reply_markup)
    return PAY


def choose_contact_info(update, context: CallbackContext) -> None:
    #context.bot.delete_message(update.effective_chat.id, context.user_data['pdf_message_id'])
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

def find_closest_salon(config, salons, location):
    distance = []
    for s in salons:
        coords = get_salon_coordinates(config, s)
        distance.append(geodesic(coords, location).m)
        print(s, geodesic(coords, location).km, coords)
    min_index = np.argmin(distance)

    return salons[min_index]


def process_payment(update, context: CallbackContext) -> None:
    context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title=context.user_data.get('salon') or 'Салон красоты',
        description='Оплата услуг',
        payload='test',
        provider_token=SBER_TOKEN,
        currency='RUB',
        prices=[
            LabeledPrice(
                context.user_data.get('service') or 'Услуги салона',
                context.user_data.get('price') or 500 * 100,
            )
        ]
    )


def precheckout_callback(update: Update, context: CallbackContext) -> None:
    query = update.pre_checkout_query
    query.answer(ok=True)


def successful_payment_callback(update: Update, context: CallbackContext) -> None:
    print('FINAL')
    user_id = str(update.effective_user.id)

    USERS[user_id]['orders'].append(
        {
            "master": context.user_data.get('master'),
            "service": context.user_data.get('service'),
            "salon": context.user_data.get('salon'),
            "date": context.user_data.get('date'),
            "slot": context.user_data.get('slot'),
        }
    )

    with open(USERS_JSON, 'w', encoding='utf-8') as users_output:
        json.dump(USERS, users_output, indent=4, ensure_ascii=False)

    update.message.reply_text("Спасибо за запись!")

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.

    updater = Updater("5939603614:AAHQRADVt5SVleCzifGK3nUH1tyJeNfZ104")
    #5837429177:AAGgLSWwHewJotuQRIyOTWGeEbjixF0DVNk
    #bot22test_bot
    #5939603614:AAHQRADVt5SVleCzifGK3nUH1tyJeNfZ104
    #bot2test_bot

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MAIN_MENU: [CallbackQueryHandler(main_submenu, pattern='0'), CallbackQueryHandler(client_area, pattern='1')],
            SHARE_LOC_REQUEST: [CallbackQueryHandler(share_location, pattern='0'), CallbackQueryHandler(client_area, pattern='1')],
            SHARE_LOC: [MessageHandler(Filters.location | Filters.regex('Нет'), get_location)],
            SERVICE_GEO: [CallbackQueryHandler(choose_service, pattern='0'), CallbackQueryHandler(main_submenu, pattern='1')],
            NEXT_STEPS: [CallbackQueryHandler(choose_salon, pattern='0'), CallbackQueryHandler(choose_service_first, pattern='1'), CallbackQueryHandler(choose_master_first, pattern='2')],
            SALON: [CallbackQueryHandler(choose_salon, pattern=r'\d+')],
            SERVICE: [CallbackQueryHandler(choose_service, pattern=r'\d+')],
            MASTER: [CallbackQueryHandler(choose_master, pattern=r'\d+')],
            ENTER_DATE: [CallbackQueryHandler(choose_date, pattern=r'\d+'), MessageHandler(Filters.text, enter_date)],
            REGISTER: [CallbackQueryHandler(register_client, pattern=r'\d+')],
            ENTER_CONTACT_INFO: [MessageHandler(Filters.contact | Filters.text, enter_phone), CallbackQueryHandler(choose_contact_info, pattern='0'), CallbackQueryHandler(start, pattern='1')],
            NAME: [MessageHandler(Filters.text, enter_name)],
            ORDERS: [CallbackQueryHandler(choose_order, pattern=r'\d+')],
            PAY: [CallbackQueryHandler(process_payment, pattern=r'\d+'), MessageHandler(Filters.successful_payment, successful_payment_callback)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    dispatcher.add_handler(conv_handler)


    # Start the Bot
    updater.start_polling()
    print('started')

if __name__ == '__main__':
    main()

