# Telegram Бот для записи в сеть салонов красоты
Сервис для онлайн записи в салоны красоты.

## Как установить
Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
Для работы создайте Telegram бота и получить его токен у [Отца Ботов](https://telegram.me/BotFather). 
Полученный ключ необходимо прописать в файле .env, как показано ниже.
```
TELEGRAM_TOKEN=токен_бота
```

## Как запустить
Для запуска бота необходимо запустить файл из консоли.
```
$ python main.py
```

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
