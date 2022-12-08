'''
Сохраняем все введенные пользователем данные в сессию.
Затем на финальном шаге сохраняем данные в json на диске.

USERS = {
    'user_id': {
        'full_name': '',
        'phone': '',
        'orders': [
            {
                'master': '',
                'service': '',
                'saloon': '',
                'date': '',
                'time': '',
            },
            {
                'master': '',
                'service': '',
                'saloon': '',
                'date': '',
                'time': '',
            },
        ]
    }
}

При входе в ЛК читаем из JSONа
'''


class Session(object):
    instances = []

    def __init__(self, user_id):
        self.user_id = user_id
        Session.instances.append(self)

        self.phone = None
        self.full_name = None
        self.order = {
            'master': None,
            'service': None,
            'saloon': None,
            'date': None,
            'time': None,
        }

    @classmethod
    def get(cls, user_id):
        return [inst for inst in cls.instances if inst.user_id == user_id]

    def save_order(self):
        #TODO save order

        Session.instances.remove(self)
