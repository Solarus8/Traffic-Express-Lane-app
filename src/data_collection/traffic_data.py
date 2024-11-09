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

def get_traffic_from_api(origin: Coordinate, destination: Coordinate) -> dict:
    url = BASE_URL.format(origin=origin, destination=destination, key=API_KEY)
    encoded_url = urllib.parse.quote(url, safe=":/?&=")
    resp = requests.get(encoded_url)
    data = resp.json()
    return data

def get_duration_in_traffic(
    origin: Coordinate, destination: Coordinate
) -> (int, int):
    data = get_traffic_from_api(origin, destination)
    routes = data["routes"]
    route = routes[0]
    legs = route["legs"]
    leg = legs[0]
    duration = leg["duration"]["value"]
    duration_in_traffic = leg["duration_in_traffic"]["value"]
    return duration, duration_in_traffic