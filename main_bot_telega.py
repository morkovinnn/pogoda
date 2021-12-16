import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

button_start = KeyboardButton('Начать')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.add(button_start)

bot =Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['Начать'])
async def process_start_command(message: types.Message):
   await message.reply('Здравствуйте, введите город, в котором хотите узнать текущую погоду.', reply_markup=greet_kb)



@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Здравствуйте, введите город, в котором хотите узнать текущую погоду.")

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождливо \U00002614",
        "Drizzle": "Дождливо \U00002614",
        "Thundershtorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328"
    }
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "\U00000001"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        await message.reply(f"----{datetime.datetime.now().strftime('%d-%m-%y %H:%M')}----\n"
              f"Погода в городе {city} на текущий момент:\nТемпература: {cur_weather}°С {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\n"
              f"Скорость ветра: {wind}м/с\nВремя рассвета: {sunrise}\nВремя заката: {sunset}\n"
              f"\n"
              f"Защити себя от коронавируса - ПОСТАВЬ ПРИВИВКУ\n"
              f"Госуслуги - проще, чем кажется\n"
              f"Не болейте!")

    except:
        await message.reply('Ошибка! Проверьте название введенного города.')



if __name__ == '__main__':
    executor.start_polling(dp)