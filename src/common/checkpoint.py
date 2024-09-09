import csv
from dataclasses import dataclass
from typing import Optional

from common.express_lane import ExpressLane, express_lanes_by_start
from utils.geometry import point_to_line_distance


@dataclass
class Checkpoint:
    start_coordinate: tuple[float, ...]
    end_coordinate: tuple[float, ...]
    express_lane_start: tuple[float, ...]

    @classmethod
    def from_coordinate(cls, coordinate: tuple[float, ...]) -> Optional["Checkpoint"]:
        for checkpoint in checkpoints:
            if checkpoint.contains_coordinate(coordinate):
                return checkpoint

    @property
    def express_lane(self) -> ExpressLane:
        return express_lanes_by_start[self.express_lane_start]

    def contains_coordinate(self, coordinate: tuple[float, ...], radius=5) -> bool:
        min_distance = point_to_line_distance(
            coordinate, self.start_coordinate, self.end_coordinate
        )
        return min_distance <= radius


checkpoints = []
with open("resources/checkpoints.csv") as f:
    reader = csv.reader(f)
    next(reader, None)  # Skip header
    for row in reader:
        points = tuple(map(float, row))
        start = tuple(points[:2])
        end = tuple(points[2:4])
        express_lane_start = tuple(points[4:])
        checkpoint = Checkpoint(start, end, express_lane_start)
        checkpoints.append(checkpoint)
