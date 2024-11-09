import json
from datetime import datetime
from time import sleep

from common.custom_types import Coordinate
from data_collection.traffic_data import get_traffic_from_api

express_lanes_file = "../Object-models/All_US36_express_lanes.json"

def print_duration_speed_traffic(data: dict):
    routes = data["routes"]
    route = routes[0]
    legs = route["legs"]
    leg = legs[0]
    distance = leg["distance"]["value"]
    duration = leg["duration"]["value"]
    duration_in_traffic = leg["duration_in_traffic"]["value"]
    miles_hr = distance / duration_in_traffic * 3600 / 1609.34  # 1 mile = 1609.34 meters, 3600 seconds = 1 hour
    print(datetime.now().isoformat(), "\nDistance:", distance, "\nAverage duration: ", duration, "seconds.\n Live traffic duration: ", duration_in_traffic, "seconds.\n  ", round(miles_hr, 2), "miles/hr average")

with open(express_lanes_file) as f:
    express_lanes = json.load(f)

#AI code to get traffic data into JSON file
results = []
for lane in express_lanes:
    lane_data = {}
    lines_start = Coordinate(lane["lines_start"]["latitude"], lane["lines_start"]["longitude"])
    lines_end = Coordinate(lane["lines_end"]["latitude"], lane["lines_end"]["longitude"])
    effective_start = Coordinate(lane["effective_start"]["latitude"], lane["effective_start"]["longitude"])
    effective_end = Coordinate(lane["effective_end"]["latitude"], lane["effective_end"]["longitude"])
    timestamp = datetime.now().isoformat()

    data = get_traffic_from_api(effective_start, effective_end)
    lane_data["effective_start_to_end"] = {
        "timestamp": timestamp,
        "lane_name": lane["lane_name"],
        "road_name": lane["road_name"],
        "direction": lane["direction"],
        "data": data
    }
    
    data2 = get_traffic_from_api(lines_start, lines_end)
    lane_data["lines_start_to_end"] = {
        "timestamp": timestamp,
        "lane_name": lane["lane_name"],
        "road_name": lane["road_name"],
        "direction": lane["direction"],
        "data": data2
    }
    
    results.append(lane_data)

with open(f'traffic_data_gmaps_api/traffic_data_mm-dd-hh-mm__{datetime.now().month}_{datetime.now().day}_{datetime.now().hour}_{datetime.now().minute}_UTC.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)
#AI code to get traffic data into JSON file


#below code prints to the console for testing
""" for lane in express_lanes:
    lines_start = Coordinate(lane["lines_start"]["latitude"], lane["lines_start"]["longitude"])
    lines_end = Coordinate(lane["lines_end"]["latitude"], lane["lines_end"]["longitude"])
    effective_start = Coordinate(lane["effective_start"]["latitude"], lane["effective_start"]["longitude"])
    effective_end = Coordinate(lane["effective_end"]["latitude"], lane["effective_end"]["longitude"])
    data = get_traffic_from_api(effective_start, effective_end)
    print(f'\n{lane["lane_name"]} {lane["road_name"]} {lane["direction"]} : effective_start to effective_end -->')
    print_duration_speed_traffic(data)
    data2 = get_traffic_from_api(lines_start, lines_end)
    print(f'{lane["lane_name"]} {lane["road_name"]} {lane["direction"]} : lines_start to lines_end -->')
    print_duration_speed_traffic(data2) """
