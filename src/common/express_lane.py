import csv
import os
from dataclasses import dataclass


@dataclass
class ExpressLane:
    start_coordinate: tuple[float, ...]
    end_coordinate: tuple[float, ...]
    route: str


express_lanes_by_start = {}
for file_name in os.listdir("resources"):
    if file_name.endswith("start and end points.csv"):
        route_name = file_name.split(" express lane")[0]
        with open(f"resources/{file_name}") as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                start = tuple(map(float, row))
                row = next(reader)
                end = tuple(map(float, row))
                express_lane = ExpressLane(start, end, route_name)
                express_lanes_by_start[start] = express_lane