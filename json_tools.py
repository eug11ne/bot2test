import json

def load_json(filename):
    with open(filename) as f:
        json_data = json.load(f)
    return json_data

def get_orders(json_data, user_name):
    orders = []
    for order in json_data[user_name]['orders']:
        orders.append(order['order_id'])
    return orders

def get_order_details(json_data, user_name, order_id):
    details = {}
    for order in json_data[user_name]['orders']:
        if order['order_id'] == order_id:
            details.update({'salon': order['salon'],
                            'service': order['service'],
                            'master': order['master']})
    return details

def get_master_names(json_data, salon):
    masters = []
    for master in json_data['MASTERS']:
        if salon in json_data['MASTERS'][master]['salons']:
            masters.append(json_data['MASTERS'][master]['name'])
    return masters

def get_salon_coordinates(json_data, salon_name):
    coordinates = []
    for salon in json_data['SALONS']:
        if json_data['SALONS'][salon]['name'] == salon_name:
            coordinates = json_data['SALONS'][salon]['coordinates']
            return coordinates



def get_all_master_names(json_data):
    masters = []
    for master in json_data['MASTERS']:
        masters.append(json_data['MASTERS'][master]['name'])
    return masters

def get_salon_names(json_data):
    salons = []
    for salon in json_data['SALONS']:
        salons.append(json_data['SALONS'][salon]['name'])
    return salons

def get_service_names(json_data):
    services = []
    for service in json_data['SERVICES']:
        services.append(json_data['SERVICES'][service]['name'])
    return services







