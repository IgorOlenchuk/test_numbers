import os
import time
import requests
import telegram
import logging

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
bot = telegram.Bot(token=TELEGRAM_TOKEN)


def parse_status(df):
    db = df['срок поставки']
    status = db['срок поставки']
    if status not in [False, True]:
        raise ValueError(f'пришел неожиданный статус: {status}')
    elif status == False:
        verdict = 'срок поставки не указан'
    elif status == True:
        verdict = 'срок поставки указан'
    return f'Результат "{db}"!\n\n{verdict}'


def get_statuses(current_timestamp):
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    data = {
        'срок поставки': current_timestamp
    }
    homework_statuses = requests.get(df, headers=headers, params=data)
    return homework_statuses.json()


def send_message(message):
    return bot.send_message(chat_id=CHAT_ID, text=message)


def main():
    current_timestamp = int(time.time())  # начальное значение timestamp

    while True:
        try:
            new_work = get_statuses(current_timestamp)
            if new_work.get('df'):
                send_message(parse_status(new_work.get('df')[3]))
            if new_work.get('срок поставки') is not None:
                current_timestamp = new_work.get('срок поставки')  # обновить timestamp
            time.sleep(600)  # опрашивать раз в десять минут

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    send_message('Start Bot')
    main()