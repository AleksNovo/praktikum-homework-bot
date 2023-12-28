# Бот-ассистент Практикум.Домашка
Учебный проект Яндекс Практикум (курс Python-разработчик)

## Описание
Telegram-бот, который обращается к API сервиса Практикум.Домашка и узнает статус вашей домашней работы: взята ли ваша домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.

Что делает бот:
- раз в 10 минут опрашивает API сервис Практикум.Домашка и проверяет статус отправленной на ревью домашней работы;
- при обновлении статуса анализирует ответ API и отправляет соответствующее уведомление в Telegram;
- логирует свою работу и сообщает о важных проблемах сообщением в Telegram.

## Технологии
[![Python](https://img.shields.io/badge/Python-3.7-3776AB?logo=python)](https://www.python.org/)
[![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-grey?logo=telegram)](https://python-telegram-bot.org/)
[![python-dotenv](https://img.shields.io/badge/python--dotenv-grey?logo=dotenv)](https://github.com/theskumar/python-dotenv)

## Запуск проекта
Клонировать репозиторий и перейти в директорию проекта:
```bash
git clone https://github.com/AleksNovo/praktikum-homework-bot.git
```
```bash
cd praktikum-homework-bot
```
Cоздать и активировать виртуальное окружение:
```bash
python -m venv venv
```
```bash
source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```
Создать в директории проекта .env файл с переменными:
```dotenv
TELEGRAM_TOKEN='<YOUR_TELEGRAM_BOT_API_TOKEN>'
PRACTICUM_TOKEN='<YOUR_PRACTICUM_API_TOKEN>'
TELEGRAM_CHAT_ID='<YOUR_TELEGRAM_USER_ID>'
```
Запустить проект:
```bash
python homework.py
```
