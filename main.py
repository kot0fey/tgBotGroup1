import random
import telebot
from telebot import types
import requests
from googletrans import Translator

TOKEN = '6340850754:AAHSk0R4RTBJM2Wh4tnCAIcJ_7Fy5ksvkwA'
bot = telebot.TeleBot(TOKEN)
WEATHER_API_KEY = '1ce32dd7ed35e3bde9621673dccc4c4f'
URL = 'https://api.telegram.org/bot'

keyboard = types.ReplyKeyboardMarkup(row_width=2)
translate_button = types.KeyboardButton('🈯Перевести')
weather_button = types.KeyboardButton('🌤Погода')
calculator_button = types.KeyboardButton('🧮Калькулятор')
mems_button = types.KeyboardButton('🤣IT мемы')
keyboard.add(translate_button, weather_button, calculator_button, mems_button)
translator = Translator(service_urls=['translate.google.com'])

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id,
                     f'<b>Здравствуйте, {message.from_user.first_name}!</b> \n Представляю вам универсального '
                     f'Telegram-бота <b>NonchBot</b>, который объединяет несколько полезных '
                     f'функций:\n1)<em>Переводчик</em>: Бот может переводить текст с английского на русский. Просто '
                     f'отправьте ему сообщение на английском, и он мгновенно вернет вам перевод на '
                     f'русский.\n2)<em>Погода</em>: Бот предоставляет информацию о погоде в выбранном городе. Просто '
                     f'укажите название города, и бот вернет текущую температуру, погодные условия и прогноз на '
                     f'ближайшие дни.\n3)<em>Калькулятор</em>: Бот имеет встроенный калькулятор для выполнения '
                     f'различных математических операций. Просто отправьте ему выражение, и бот рассчитает '
                     f'результат.\n4)<em>IT-мемы</em>: Для поднятия настроения, бот может присылать вам мемы на тему '
                     f'IT. Получите порцию юмора и отдохните от работы или учебы.\n<b>Выберите действие на панели '
                     f'команд</b>',
                     parse_mode='HTML', reply_markup=keyboard)


# Обработчик команды /info
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id,
                     '<b>Разработка компании Nonch Inc.</b>\nРазработчики:\n<b>Пруц Константин Андреевич и Соколов '
                     'Никита Валерьевич</b>\nСанкт-Петербург 2023 ',
                     parse_mode='HTML')


# Функция для отображения кнопок
def show_buttons(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "Выберите действие на панели команд", reply_markup=keyboard)


# Обработчик выбора "Перевести"
@bot.message_handler(func=lambda message: message.text == '🈯Перевести')
def translate_text(message):
    bot.send_message(message.chat.id, 'Введите текст, который нужно перевести:', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, process_translation)


def process_translation(message):
    if message.text:
        text_to_translate = message.text
        translation = translator.translate(text_to_translate, dest='ru')
        bot.send_message(message.chat.id, f'Перевод:\n{translation.text}')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите текст для перевода.')
    show_buttons(message)


# Обработчик выбора "Погода"
@bot.message_handler(func=lambda message: message.text == '🌤Погода')
def handle_weather(message):
    bot.send_message(message.chat.id, 'Введите название города:', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_weather)


def get_weather(message):
    city = message.text.strip()
    weather_data = fetch_weather(city)

    if weather_data:
        temperature = weather_data['main']['temp']
        pressure = weather_data['main']['pressure']
        wind_speed = weather_data['wind']['speed']
        weather_status = translator.translate(weather_data['weather'][0]['description'], src='en', dest='ru').text
        response = f"Погода в {city}:\n"
        response += f"Температура: {temperature} °C\n"
        response += f"Давление: {pressure} hPa\n"
        response += f"Скорость ветра: {wind_speed} м/с\n"
        response += f"Статус: {weather_status}\n"
    else:
        response = "Город не найден."

    bot.send_message(message.chat.id, response)
    show_buttons(message)


def fetch_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        weather_data = response.json()
        if weather_data["cod"] != "404":
            return weather_data
    except:
        pass
    return None


# Обработчик выбора "Калькулятор"
@bot.message_handler(func=lambda message: message.text == '🧮Калькулятор')
def handle_calculator(message):
    bot.send_message(message.chat.id, 'Введите математическое выражение:', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, calculate_expression)


def calculate_expression(message):
    expression = message.text
    try:
        result = eval(expression)
        if isinstance(result, (int, float)) and result == float('inf'):
            raise ZeroDivisionError('Деление на ноль')
        bot.send_message(message.chat.id, f'Результат: {result}')
        show_buttons(message)
    except ZeroDivisionError:
        bot.send_message(message.chat.id, 'Ошибка: Деление на ноль')
        show_buttons(message)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при вычислении выражения')
        show_buttons(message)


# Обработчик выбора "🤣IT мемы"
@bot.message_handler(func=lambda message: message.text == '🤣IT мемы')
def send_meme(message):
    public = random.randint(100, 303)
    chat_id = message.chat.id
    img_url = f'https://t.me/itshnik_mem/{public}'
    request_url = f'{URL}{TOKEN}/sendPhoto?chat_id={chat_id}&photo={img_url}'
    response = requests.get(request_url)


# Обработчик неизвестной команды
@bot.message_handler(func=lambda message: True)
def handle_unknown_command(message):
    bot.reply_to(message, "Извините, я не понимаю эту команду. Пожалуйста, введите корректную команду.")


# Запуск бота
bot.polling()
