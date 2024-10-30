import json
from datetime import datetime
from time import sleep

from common.custom_types import Coordinate
from data_collection.traffic_data import get_traffic, get_traffic_from_api

# Lowell (West Bound)
lines_start = Coordinate(39.835657, -105.022941)
lines_end = Coordinate(39.842883, -105.040233)
effective_start = Coordinate(39.835657, -105.022941)
effective_end = Coordinate(39.842883, -105.040233)

def print_duration_speed_traffic(data: dict):
    
    routes = data["routes"]
    route = routes[0]
    legs = route["legs"]
    leg = legs[0]
    distance = leg["distance"]["value"]
    duration = leg["duration"]["value"]
    duration_in_traffic = leg["duration_in_traffic"]["value"]
    miles_hr = distance / duration_in_traffic * 3600 / 1609.34
    print(datetime.now(), duration_in_traffic, round(miles_hr, 2))


while True:
    data = get_traffic_from_api(effective_start, effective_end)
    print_duration_speed_traffic(data)
    data2 = get_traffic_from_api(lines_start, lines_end)
    print_duration_speed_traffic(data2)

    sleep(60 * 3)
