from typing import NamedTuple
from geopy.geocoders import Nominatim  # type: ignore
import config  # type: ignore
from exceptions import CantGetCoordinates


class Coordinate(NamedTuple):
    latitude: float
    longitude: float


def get_address_coordinates() -> Coordinate:
    coordinates = _get_geopy_coordinates()
    return _round_coordinates(coordinates)


def _get_geopy_coordinates() -> Coordinate:
    geopy_output = _get_geopy_output()
    coordinates = _parse_coord(geopy_output)
    return coordinates


def _get_geopy_output() -> dict[str, str]:
    nominatim = Nominatim(user_agent=config.USER_AGENT)
    output = nominatim.geocode(config.ADDRESS).raw
    return output


def _parse_coord(output: dict[str, str]) -> Coordinate:
    latitude = _parse_float_coordinates(output['lat'])
    longitude = _parse_float_coordinates(output['lon'])
    return Coordinate(latitude, longitude)


def _parse_float_coordinates(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise CantGetCoordinates


def _round_coordinates(coordinates: Coordinate) -> Coordinate:
    if not config.USE_ROUNDED_COORDINATES:
        return coordinates
    return Coordinate(*map(
        lambda x: round(x, 1),
        [coordinates.latitude, coordinates.longitude]
    ))


if __name__ == '__main__':
    print(get_address_coordinates())
