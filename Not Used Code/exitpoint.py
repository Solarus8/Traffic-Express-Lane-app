import csv
from dataclasses import dataclass
from typing import Optional

from common.custom_types import Coordinate
from common.express_lane import ExpressLane, express_lanes_by_start
from utils.geometry import is_point_in_quadrilateral


@dataclass
class Exitpoint:
    name: str
    points: tuple[Coordinate, ...]

    @classmethod
    def from_coordinate(cls, coordinate: Coordinate) -> Optional["Exitpoint"]:
        for exitpoint in exitpoints:
            if exitpoint.contains_coordinate(coordinate):
                return exitpoint

    @property
    def express_lane(self) -> ExpressLane:
        return express_lanes_by_start[self.express_lane_start]

    def contains_coordinate(self, coordinate: Coordinate) -> bool:
        return is_point_in_quadrilateral(tuple(coordinate), self.points)


exitpoints = []
with open("resources/exitpoints.csv") as f:
    reader = csv.reader(f)
    next(reader, None)  # Skip header
    exitpoint = None
    for row in reader:
        point = Coordinate(*map(float, row[:2]))
        name = row[2]
        if name:
            exitpoint = Exitpoint(name, (point,))
            exitpoints.append(exitpoint)
        else:
            exitpoint.points = exitpoint.points + (point,)
