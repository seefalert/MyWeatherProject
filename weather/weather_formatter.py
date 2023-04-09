from weather_api_service import Weather


def format_weather(weather: Weather) -> str:
    return (f'{weather.city} температура {weather.temperature}°С, '
            f'{weather.weather_type.value}\n'
            f'Скорость ветра: {weather.wind_speed} м/с\n'
            f'Восход: {weather.sunrise.strftime("%H:%M")}\n'
            f'Закат: {weather.sunset.strftime("%H:%M")}')


if __name__ == '__main__':
    from datetime import datetime
    from weather_api_service import WeatherType
    print(format_weather(Weather(
        temperature=10,
        weather_type=WeatherType.CLEAR,
        wind_speed=5,
        sunrise=datetime.fromisoformat('2023-04-09 04:00:00'),
        sunset=datetime.fromisoformat('2023-04-09 20:00:00'),
        city='Санкт-Петербург'
    )))
