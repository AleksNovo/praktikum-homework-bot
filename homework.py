import logging
import os
import sys
import time
import requests
from dotenv import load_dotenv
from http import HTTPStatus

from telegram import Bot


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(message)s',
    handlers=[logging.FileHandler('log.txt'),
              logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

ENV_VARS = ['PRACTICUM_TOKEN', 'TELEGRAM_TOKEN', 'TELEGRAM_CHAT_ID']

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

ERROR_API_MESSAGE = "API возвращает код, отличный от 200:"
CHECK_TOKENS_ERROR = "Требуемые переменные окружения отсутствуют:"

def send_message(bot, message):
    """Отправляет сообщение в Telegram чат по TELEGRAM_CHAT_ID."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info(f"Отправка сообщения в Телеграмм: '{message}'")
    except Exception:
        logger.error("Сбой отправки сообщения в Телеграмм")


def get_api_answer(current_timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса."""
    timestamp = current_timestamp
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except Exception as error:
        logging.error(f"Сервер yandex.practicum вернул ошибку: {error}")

    if response.status_code != HTTPStatus.OK:
        status_code = response.status_code
        logging.error(f"{ERROR_API_MESSAGE} {status_code}")
        raise Exception(f"{ERROR_API_MESSAGE} {status_code}")

    try:
        return response.json()
    except ValueError:
        logging.error("Ответ от сервера должен быть в формате JSON")


def check_response(response):
    """
    Проверяет ответ API на корректность.
    Если ответ соответствует, возвращает список
    домашних работ.
    """
    try:
        homework = response['homeworks']
    except KeyError:
        message = "Ответ от API не содержит ключ 'homeworks'."
        logging.error(message)
        raise KeyError(message)
    except IndexError:
        message = "Задания не найдены. Пустой список."
        logging.error(message)
        raise IndexError(message)

    if not isinstance(homework, list):
        logging.error("Homeworks не является списком")
        return TypeError(message)

    return homework


def parse_status(homework):
    """Извлекает из информации о домашней работе статус этой работы."""
    homework_name = homework.get('homework_name')
    try:
        homework_status = homework['status']
    except KeyError:
        logging.error(f'Отсутствует ключ {homework_status} в статусах работы')

    if homework_status not in HOMEWORK_STATUSES:
        raise KeyError(f'Отсутствует ключ {homework_status} в статусах работы')
    if homework_status in HOMEWORK_STATUSES:
        verdict = HOMEWORK_STATUSES.get(homework_status)
        if not verdict:
            logging.error('Отсутствие ожидаемых ключей в ответе API.')
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяет доступность переменных окружения."""
    undefined_vars = set(filter(lambda v: not globals().get(v), ENV_VARS))
    if not undefined_vars:
        return True
    logging.error(f'{CHECK_TOKENS_ERROR} {undefined_vars}')
    return False


def main():
    """Основная логика работы бота."""
    if check_tokens():
        bot = Bot(token=TELEGRAM_TOKEN)
        current_timestamp = int(time.time()) - 100000
        last_error = ""

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if len(homeworks) > 0:
                message = parse_status(homeworks[0])
                send_message(bot, message)
            else:
                logging.info("Домашние задания не найдены.")
            current_timestamp = response.get('current_date')

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.critical(message)
            if last_error != message and 'Сбой отправки' not in message:
                send_message(bot, message)
                last_error = message
            logging.error(message)
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.critical('Выход из программы по Ctrl-C')
        sys.exit(0)
