import telebot
from telebot import types

API_TOKEN = '7459858308:AAHDzrATTJ04FUB8J33FlLtdxja-Hw1dro0'  # Замените на токен вашего бота
CHANNEL_ID = '@dfgsdfgfsdd'  # Замените на ID вашего канала

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Саратов")
    item2 = types.KeyboardButton("Энгельс")
    markup.add(item1, item2)

    bot.send_message(message.chat.id, "В каком городе рассматриваете отдых?", reply_markup=markup)
    bot.register_next_step_handler(message, select_game)

def select_game(message):
    city = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Гидробол")
    item2 = types.KeyboardButton("Пейнтбол")
    item3 = types.KeyboardButton("Лазертаг")
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, "В какую игру вы хотели бы сыграть?", reply_markup=markup)
    bot.register_next_step_handler(message, get_date, city)

def get_date(message, city):
    game = message.text
    bot.send_message(message.chat.id, "В какую дату вы бы хотели поиграть? Укажите дату в формате ДД.ММ.ГГГГ.")
    bot.register_next_step_handler(message, get_phone, city, game)

def get_phone(message, city, game):
    date = message.text
    bot.send_message(message.chat.id, "Пожалуйста, введите номер телефона (в формате 89001112233):")
    bot.register_next_step_handler(message, confirm_order, city, game, date)

def confirm_order(message, city, game, date):
    phone = message.text

    order_details = (
        f"Заявка от {message.from_user.first_name}:\n"
        f"Город: {city}\n"
        f"Игра: {game}\n"
        f"Дата: {date}\n"
        f"Телефон: {phone}\n"
    )

    # Отправка заказа в канал
    bot.send_message(CHANNEL_ID, order_details)

    bot.send_message(message.chat.id, "Ваша заявка оформлена и отправлена администратору. Спасибо!")
bot.polling(none_stop=True)