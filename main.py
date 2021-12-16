import requests
import datetime
from pprint import pprint
from config import open_weather_token


def get_weather(city, open_weather_token):

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
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        pprint(data)

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

        print(f"----{datetime.datetime.now().strftime('%d-%m-%y %H:%M')}----\n"
              f"Погода в городе {city} на текущий момент:\nТемпература: {cur_weather}°С {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\n"
              f"Скорость ветра: {wind}м/с\nВремя рассвета: {sunrise}\nВремя заката: {sunset}\n"
              f"\n"
              f"Защити себя от коронавируса - ПОСТАВЬ ПРИВИВКУ\n"
              f"Госуслуги - проще, чем кажется\n"
              f"Не болейте!")

    except Exception as ex:
        print(ex)
        print('Ошибка! Проверьте название введенного города.')



def main():
    city = input("Введите необходимый город: ")
    get_weather(city, open_weather_token)

if __name__ == '__main__':
    main()