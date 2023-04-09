from typing import NamedTuple, Literal
from datetime import datetime
from enum import Enum
import urllib.request
from urllib.error import URLError
from json.decoder import JSONDecodeError
import ssl
import json

from coordinates import Coordinate
import config  # type: ignore
from exceptions import ApiServiceError

Celsius = int
meters_second = int


class WeatherType(Enum):
    THUNDERSTORM = 'Гроза'
    DRIZZLE = 'Изморозь'
    RAIN = 'Дождь'
    SNOW = 'Снег'
    CLEAR = 'Ясно'
    FOG = 'Туман'
    CLOUDS = 'Облачно'


class Weather(NamedTuple):
    temperature: Celsius
    weather_type: WeatherType
    wind_speed: meters_second
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordinates: Coordinate) -> Weather:
    openweather_response = _get_openweather_response(
        latitude=coordinates.latitude, longitude=coordinates.longitude)
    weather = _parce_openweather_response(openweather_response)
    return weather


def _get_openweather_response(latitude: float, longitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.OPENWEATHER_URL.format(
        latitude=latitude, longitude=longitude)
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise ApiServiceError


def _parce_openweather_response(openweather_response: str) -> Weather:
    try:
        openweather_dict = json.loads(openweather_response)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(
        temperature=_parce_temperature(openweather_dict),
        weather_type=_parce_weather_type(openweather_dict),
        wind_speed=_parce_wind_speed(openweather_dict),
        sunrise=_parce_sun_time(openweather_dict, 'sunrise'),
        sunset=_parce_sun_time(openweather_dict, 'sunset'),
        city=config.ADDRESS_FOR_USER
    )


def _parce_temperature(openweather_dict: dict) -> Celsius:
    return round(openweather_dict['main']['temp'])


def _parce_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict['weather'][0]['id'])
    except (IndexError, KeyError):
        raise ApiServiceError
    weather_type = {
        '1': WeatherType.THUNDERSTORM,
        '3': WeatherType.DRIZZLE,
        '5': WeatherType.RAIN,
        '6': WeatherType.SNOW,
        '7': WeatherType.FOG,
        '800': WeatherType.CLEAR,
        '80': WeatherType.CLOUDS,
    }
    for _id, _weather_type in weather_type.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise ApiServiceError


def _parce_sun_time(
        openweather_dict: dict,
        time: Literal['sunrise'] | Literal['sunset']) -> datetime:
    return datetime.fromtimestamp(openweather_dict['sys'][time])


def _parce_wind_speed(openweather_dict: dict) -> meters_second:
    return round(openweather_dict['wind']['speed'])


if __name__ == '__main__':
    print(get_weather(Coordinate(59.9, 30.3)))
