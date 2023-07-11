import telebot
from telebot import types


TOKEN = '6340850754:AAHSk0R4RTBJM2Wh4tnCAIcJ_7Fy5ksvkwA'
bot = telebot.TeleBot(TOKEN)


keyboard = types.ReplyKeyboardMarkup(row_width=2)
translate_button = types.KeyboardButton('🈯Перевести')
weather_button = types.KeyboardButton('🌤Погода')
calculator_button = types.KeyboardButton('🧮Калькулятор')
mems_button = types.KeyboardButton('🤣IT мемы')
keyboard.add(translate_button, weather_button, calculator_button, mems_button)

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





# Обработчик выбора "Перевести"
@bot.message_handler(func=lambda message: message.text == '🈯Перевести')



# Обработчик выбора "Погода"
@bot.message_handler(func=lambda message: message.text == '🌤Погода')



# Обработчик выбора "Калькулятор"
@bot.message_handler(func=lambda message: message.text == '🧮Калькулятор')



# Обработчик выбора "🤣IT мемы"
@bot.message_handler(func=lambda message: message.text == '🤣IT мемы')



# Обработчик неизвестной команды
@bot.message_handler(func=lambda message: True)
def handle_unknown_command(message):
    bot.reply_to(message, "Извините, я не понимаю эту команду. Пожалуйста, введите корректную команду.")


# Запуск бота
bot.polling()
