import telebot
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from datetime import datetime

# Загрузка данных из файла .env
load_dotenv()

# Чтение токена из файла .env
token = os.getenv("TOKEN")

# Путь к файлу с подписанными пользователями
users_file = 'users_sub.txt'
# Путь к файлу с отзывами
reviews_file = 'reviews.txt'

# Список пользователей, подписанных на обновления конфига
subscribed_users = []

# Создаем экземпляр бота
bot = telebot.TeleBot(token)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id in subscribed_users:
        bot.reply_to(message, '📝 Оставить отзыв /rev\n\n📖 Подробнее /help')
    else:
        bot.send_message(chat_id, 'Приветик!, что бы скачать конфиг нужно подписаться 🥺\n\n📖 Подробнее /help')

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id in subscribed_users:
        bot.reply_to(message, '📥 Скачать конфиг - /Download\n📄 Инструкция по установки конфига - /insc\n\n📝 Оставить отзыв /rev\n🗒️ Отзывы /rev_list\n\n🔧 Тех.Поддержка - /fix')
    else:
        bot.send_message(chat_id, '🧾 Подписаться - /ok\n🗒️ Отзывы /rev_list\n\n🔧 Тех.Поддержка - /fix')

@bot.message_handler(commands=['ok'])
def subscribe(message):
    user_id = message.from_user.id
    if user_id not in subscribed_users:
        subscribed_users.append(user_id)
        with open(users_file, 'a') as file:
            file.write(str(user_id) + '\n')
        bot.reply_to(message, '💜 Спасибки за подписку!\n📥 Скачать конфиг Бруснички /Download')
        bot.send_message(message.chat.id, '[Подпишитесь на канал](https://t.me/brusnikaone).', parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, 'Ты уже подписан(а) 🥰')

# Обработчик команды /ne_ok
@bot.message_handler(commands=['ne_ok'])
def unsubscribe(message):
    user_id = message.from_user.id
    if user_id in subscribed_users:
        subscribed_users.remove(user_id)
        with open(users_file, 'r') as file:
            lines = file.readlines()
        with open(users_file, 'w') as file:
            for line in lines:
                if line.strip() != str(user_id):
                    file.write(line)
        bot.reply_to(message, '😢 Ты отписался(ась)')
    else:
        bot.reply_to(message, '😕 Ты не подписан(а)')

# Обработчик команды /Download
@bot.message_handler(commands=['Download'])
def send_cfg(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id in subscribed_users:
        if os.path.exists('config.zip'):
            # Получение даты последней модификации файла
            file_modified = os.path.getmtime('config.zip')
            # Преобразование времени в формат даты
            file_date = datetime.fromtimestamp(file_modified).strftime('%d.%b')
            bot.send_document(chat_id, open('config.zip', 'rb'), caption=f'L.UPD: {file_date}\n\n🗃️ Конфиг в архиве.\n❔ Как установить.\n       смотрите инструкцию. /insc')
        else:
            bot.send_message(chat_id, '🙁 К сожалению, конфиг на проверке, ожидайте...')
    else:
        bot.send_message(chat_id, 'Для скачивания конфига необходимо подписаться 🥺\nКоманда /ok')

# Обработчик команды /insc
@bot.message_handler(commands=['insc'])
def send_instruction(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id in subscribed_users:
        bot.send_document(chat_id, open('instruction.txt', 'rb'), caption='Читайте ВНИМАТЕЛЬНО ❗️')
    else:
        bot.send_message(chat_id, 'Для просмотра инструкции необходимо подписаться 🥺\nКоманда /ok')

def save_subscribed_users():
    with open('users_sub.txt', 'w') as file:
        for user_id in subscribed_users:
            file.write(str(user_id) + '\n')

def load_subscribed_users():
    try:
        with open('users_sub.txt', 'r') as file:
            for line in file:
                if line.strip():
                    user_id = int(line.strip())
                    subscribed_users.append(user_id)
    except FileNotFoundError:
        pass

# Обработчик команды /fix
@bot.message_handler(commands=['fix'])
def tech_support(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Обратитесь к [Разработчику](t.me/myp_official)', parse_mode='Markdown')

# Функция для отправки сообщения подписчикам
def send_message_to_subscribers(message_text):
    for user_id in subscribed_users:
        chat_member = bot.get_chat_member(chat_id, user_id)
        if chat_member.status not in ['left', 'kicked']:
            bot.send_message(user_id, message_text)

# функция обработки комманды /snd_all
@bot.message_handler(commands=['snd'])
def send_to_all(message):
    if message.from_user.id == YOU_CHAT_ID:
        message_text = message.text.replace('/snd', '')
        if message_text:
            send_message_to_subscribers(message_text)
            bot.reply_to(message, 'Сообщение отправлено всем подписчикам.')
        else:
            bot.reply_to(message, 'Сообщение пустое.')
    else:
        bot.reply_to(message, '⛔️ Доступ закрыт.')

def send_message_to_subscribers(message_text):
    for user_id in subscribed_users:
        if user_id != 1132585602:
            bot.send_message(user_id, message_text)

# счетчик подписок
@bot.message_handler(commands=['sids'])
def scored_users(message):
    with open("users_sub.txt", 'r') as fp:
        lines = [line.strip() for line in fp if line.strip()]
        count = len(lines)
        if message.from_user.id == YOU_CHAT_ID:
            bot.reply_to(message, f"Кол-во ягодок: {count}")
        else:
            bot.reply_to(message, '⛔️ Доступ закрыт.')

# Обработчик команды /rev
@bot.message_handler(commands=['rev'])
def add_review(message):
    user_id = message.from_user.id
    username = message.from_user.username
    if user_id in subscribed_users:
        review_text = message.text.replace('/rev', '')
        if review_text:
            with open(reviews_file, 'a') as file:
                file.write(f'Отзыв от {username}:\n{review_text}\n\n')
            bot.reply_to(message, '💜 Спасибо за Ваш отзыв о конфиге!')
        else:
            bot.reply_to(message, '📝 Что бы оставить отзыв напишите: /rev тут ваш отзыв')
    else:
        bot.send_message(message.chat.id, 'Чтобы оставить отзыв, необходимо подписаться 🥺\nКоманда /ok')

# Обработчик команды /rev_list
@bot.message_handler(commands=['rev_list'])
def show_reviews(message):
    with open(reviews_file, 'r') as file:
        reviews = file.read()
        if reviews:
            bot.send_message(message.chat.id, "🗒️ Отзывы:\n\n" + reviews)
        else:
            bot.send_message(message.chat.id, "☹️ Отзывов пока нет.")

def load_reviews():
    try:
        with open(reviews_file, 'r') as file:
            pass
    except FileNotFoundError:
        with open(reviews_file, 'w') as file:
            pass

# checker
@bot.message_handler(commands=['/'])
def check(message):
    if message.from_user.id == YOU_CHAT_ID:
        bot.reply_to(message, "ok")

load_subscribed_users()
load_reviews()

print("ok.")

# Запускаем бота
bot.polling(none_stop=True)
