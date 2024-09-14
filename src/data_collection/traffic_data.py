import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GOOGLE_API_KEY")
BASE_URL = (
    "https://maps.googleapis.com/maps/api/directions/json?"
    "origin={origin}&destination={destination}&departure_time=now&key={key}&traffic_model=best_guess"
)


def get_traffic_from_api(origin, destination) -> dict:
    url = BASE_URL.format(origin=origin, destination=destination, key=API_KEY)
    resp = requests.get(url)
    data = resp.json()
    with open(f"traffic_data/{origin}_{destination}.json", "w") as f:
        json.dump(data, f, indent=2)
    return data


def get_traffic_from_file(origin, destination) -> dict:
    path = f"traffic_data/{origin}_{destination}.json"
    with open(path) as f:
        data = json.load(f)
    return data


def get_traffic(origin, destination) -> dict:
    try:
        data = get_traffic_from_file(origin, destination)
    except FileNotFoundError:
        data = get_traffic_from_api(origin, destination)
    return data


def get_traffic_rating(origin, destination) -> float:
    """Return a float value of how many times the trip takes longer because of traffic."""
    data = get_traffic(origin, destination)
    routes = data["routes"]
    print("routes:", len(routes), routes)
    route = routes[0]
    legs = route["legs"]
    print("legs:", len(legs), legs)
    leg = legs[0]
    duration = leg["duration"]["value"]
    print("duration:", duration)
    duration_in_traffic = leg["duration_in_traffic"]["value"]
    print("duration_in_traffic:", duration_in_traffic)
    return duration_in_traffic / duration


if __name__ == "__main__":
    ORIGIN = "RXHX%2BW52,+Twin+Lakes,+CO+80221,+USA"
    DESTINATION = "39.834298,-105.0189317"
    print(get_traffic_rating(ORIGIN, DESTINATION))
