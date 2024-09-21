import csv
from dataclasses import dataclass
from typing import Optional

from common.custom_types import Coordinate
from common.express_lane import ExpressLane, express_lanes_by_start
from utils.geometry import is_point_in_quadrilateral


@dataclass
class Checkpoint:
    points: tuple[Coordinate, ...]
    express_lane_start: Coordinate

    @classmethod
    def from_coordinate(cls, coordinate: Coordinate) -> Optional["Checkpoint"]:
        for checkpoint in checkpoints:
            if checkpoint.contains_coordinate(coordinate):
                return checkpoint

    @property
    def express_lane(self) -> ExpressLane:
        return express_lanes_by_start[self.express_lane_start]

    def contains_coordinate(self, coordinate: Coordinate) -> bool:
        return is_point_in_quadrilateral(tuple(coordinate), self.points)


checkpoints = []
with open("resources/checkpoints.csv") as f:
    reader = csv.reader(f)
    next(reader, None)  # Skip header
    for row in reader:
        a = Coordinate(*map(float, row[:2]))
        express_lane_start = tuple(map(float, row[2:]))
        next(reader, None)
        b = Coordinate(*map(float, row[:2]))
        next(reader, None)
        c = Coordinate(*map(float, row[:2]))
        next(reader, None)
        d = Coordinate(*map(float, row[:2]))
        checkpoint = Checkpoint((a, b, c, d), Coordinate(*express_lane_start))
        checkpoints.append(checkpoint)
