import requests
import json


def city_weather(city_name, api_key):
    service = 'https://api.openweathermap.org/data/2.5/weather'
    try:
        req = requests.get(f'{service}?q={city_name}&appid={api_key}&units=metric&lang=ru')
        weather = json.loads(req.text)
        return (f"Погода в городе {city_name}: облачность - {weather['weather'][0]['description']}, температура - "
                f"{weather['main']['temp']}, ощущается как {weather['main']['feels_like']}")
    except IOError:
        return f'Проблемы с сетью.'
    except KeyError:
        return f'Данные не введены'


city = input('Введите город: ')
api = input('Введите api ключ. Я отправила его в коммнетах с домашкой: ')

print(city_weather(city, api))
