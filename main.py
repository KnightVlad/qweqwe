import telebot
import datetime
from pyowm import OWM
from pyowm.utils.config import get_default_config

bot = telebot.TeleBot('5619677695:AAH54V9IA2p61OP9LSGEPz5Vo-7usZNE6mY')

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('привет', 'пока', 'time', 'погода', '/start')
mgr = 0
weather = False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global mgr

    try:
        language = get_default_config()
        language['language'] = 'ru'
        owm = OWM('dd280816f238abb015c15f17c65ae28b', language)
        mgr = owm.weather_manager()
    except:
        bot.send_message(message.chat.id, 'No', reply_markup=keyboard1)

    bot.send_message(message.chat.id, 'Привет, ты написал/start', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    global weather
    if weather:
        try:
            observation = mgr.weather_at_place(message.text)
            weather = observation.weather
            bot.send_message(message.chat.id, f'''Сейчас на улице: {weather.detailed_status}
Облачность: {weather.clouds}%
Текущая температура: {weather.temperature("celsius").get("temp")} градусов
Максимальная температура: {weather.temperature("celsius").get("temp_max")} градусов
Минимальная температура: {weather.temperature("celsius").get("temp_min")} градусов
Сейчас ощущается: {weather.temperature("celsius").get("feels_like")} градусов
За последний час выпало осадков: {weather.rain.get("1h", "0")} мм
Скорость ветра: {weather.wind().get("speed")} м/с''')
        except:
            bot.send_message(message.chat.id, 'No')

        weather = False
    else:
        if message.text.lower() == 'привет':
            bot.send_message(message.chat.id, 'И тебе привет!')
        elif message.text.lower() == 'пока':
            bot.send_message(message.chat.id, 'И тебе пока!')
        elif message.text.lower() == 'time':
            day = datetime.datetime.now().isoweekday()
            if day == 1:
                day = 'понедельник'
            elif day == 2:
                day = 'вторник'
            elif day == 3:
                day = 'среда'
            elif day == 4:
                day = 'четверг'
            elif day == 5:
                day = 'пятница'
            elif day == 6:
                day = 'суббота'
            elif day == 7:
                day = 'воскресенье'
            bot.send_message(message.chat.id, f'{day}')
            now = datetime.datetime.now()
            if now.day < 10:
                day = f'0{now.day}'
            else:
                day = now.day
            if now.month < 10:
                month = f'0{now.month}'
            else:
                month = now.month
            bot.send_message(message.chat.id, f'{day}-{month}-{now.year} {now.hour + 3}:{now.minute}')
        elif message.text.lower() == 'погода':
            bot.send_message(message.chat.id, 'Введите город')
            weather = True


bot.polling()
