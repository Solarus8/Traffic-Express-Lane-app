import csv
from dataclasses import dataclass

from common.custom_types import Coordinate
from common.express_lane import ExpressLane, express_lanes_by_start


@dataclass
class Gate:
    name: str
    points: (Coordinate, Coordinate)
    express_lane_start: Coordinate

    @classmethod
    def by_name(cls, name: str) -> "Gate":
        for gate in gates:
            if gate.name == name:
                return gate

    @property
    def express_lane(self) -> ExpressLane:
        return express_lanes_by_start[self.express_lane_start]


gates = []
with open("resources/gates.csv") as f:
    reader = csv.reader(f)
    next(reader, None)  # Skip header
    for row in reader:
        name = row[0]
        a = Coordinate(*map(float, row[1:3]))
        express_lane_start = tuple(map(float, row[3:5]))
        next(reader, None)
        b = Coordinate(*map(float, row[1:3]))
        gate = Gate(name, (a, b), Coordinate(*express_lane_start))
        gates.append(gate)
