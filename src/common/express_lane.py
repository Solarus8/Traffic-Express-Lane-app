import csv
import os
from dataclasses import dataclass

from common.custom_types import Coordinate


@dataclass
class ExpressLane:
    name: str
    start_coordinate: Coordinate
    end_coordinate: Coordinate
    route: str


express_lanes_by_start = {}
for file_name in os.listdir("resources"):
    if file_name.endswith("start and end points.csv"):
        route_name = file_name.split(" express lane")[0]
        with open(f"resources/{file_name}") as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                name = row.pop()
                start = Coordinate(*map(float, row))
                row = next(reader)
                row.pop()  # Remove redundant name
                end = Coordinate(*map(float, row))
                express_lane = ExpressLane(name, start, end, route_name)
                express_lanes_by_start[start] = express_lane
