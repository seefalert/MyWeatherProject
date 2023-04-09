from pathlib import Path

from coordinates import get_address_coordinates
from weather_api_service import get_weather
from weather_formatter import format_weather
from exceptions import CantGetCoordinates, ApiServiceError
from history import save_weather, PlainFileWeatherStorage, JSONFileWeatherStorage


def main():
    try:
        coordinates = get_address_coordinates()
    except CantGetCoordinates:
        print('Не удалось получить координаты')
        exit(1)
    try:
        weather = get_weather(coordinates)
    except ApiServiceError:
        print('Не удалось получить погоду')
        exit(1)
    print(format_weather(weather))

    save_weather(
        weather,
        PlainFileWeatherStorage(Path.cwd() / 'history.txt')
    )
    save_weather(
        weather,
        JSONFileWeatherStorage(Path.cwd() / 'history.json')
    )


if __name__ == '__main__':
    main()
