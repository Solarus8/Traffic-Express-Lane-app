import json
import os
import urllib.parse

import requests
from dotenv import load_dotenv

from common.custom_types import Coordinate

load_dotenv()

API_KEY = os.environ.get("GOOGLE_API_KEY")
BASE_URL = (
    "https://maps.googleapis.com/maps/api/directions/json?"
    "origin={origin}&destination={destination}&departure_time=now&key={key}&traffic_model=best_guess"
)


base_directory = "traffic_data"
if not os.path.exists(base_directory):
    os.makedirs(base_directory)


def get_traffic_from_api(origin: Coordinate, destination: Coordinate) -> dict:
    url = BASE_URL.format(origin=origin, destination=destination, key=API_KEY)
    encoded_url = urllib.parse.quote(url, safe=":/?&=")
    resp = requests.get(encoded_url)
    data = resp.json()
    with open(f"{base_directory}/{origin}_{destination}.json", "w") as f:
        json.dump(data, f, indent=2)
    return data


def get_traffic_from_file(origin: Coordinate, destination: Coordinate) -> dict:
    path = f"{base_directory}/{origin}_{destination}.json"
    with open(path) as f:
        data = json.load(f)
    return data


def get_traffic(origin: Coordinate, destination: Coordinate) -> dict:
    try:
        data = get_traffic_from_file(origin, destination)
    except FileNotFoundError:
        data = get_traffic_from_api(origin, destination)
    return data


def get_duration_in_traffic(
    origin: Coordinate, destination: Coordinate
) -> (float, float):
    data = get_traffic(origin, destination)
    routes = data["routes"]
    route = routes[0]
    legs = route["legs"]
    leg = legs[0]
    duration = leg["duration"]["value"]
    duration_in_traffic = leg["duration_in_traffic"]["value"]
    return duration, duration_in_traffic


def get_traffic_rating(origin: Coordinate, destination: Coordinate) -> float:
    """Return a float value of how many times the trip takes longer because of traffic."""
    duration, duration_in_traffic = get_duration_in_traffic(origin, destination)
    return duration_in_traffic / duration


if __name__ == "__main__":
    ORIGIN = "RXHX%2BW52,+Twin+Lakes,+CO+80221,+USA"
    DESTINATION = "39.834298,-105.0189317"
    print(get_traffic_rating(ORIGIN, DESTINATION))
