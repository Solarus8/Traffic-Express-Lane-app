import json
from datetime import datetime
from time import sleep

from common.custom_types import Coordinate
from data_collection.traffic_data import get_traffic, get_traffic_from_api

# Lowell (West Bound)
start = Coordinate(39.835657, -105.022941)
end = Coordinate(39.842883, -105.040233)


for i in range(20):
    data = get_traffic_from_api(start, end)

    # print(json.dumps(data, indent=2))
    routes = data["routes"]
    route = routes[0]
    legs = route["legs"]
    leg = legs[0]
    distance = leg["distance"]["value"]
    duration = leg["duration"]["value"]
    duration_in_traffic = leg["duration_in_traffic"]["value"]
    km_h = distance / duration_in_traffic * 3.6
    print(datetime.now(), duration_in_traffic, round(km_h, 2))

    sleep(60 * 30)
