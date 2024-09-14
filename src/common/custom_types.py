from dataclasses import dataclass


@dataclass
class Coordinate:
    latitude: float
    longitude: float

    def __str__(self):
        return ",".join(map(str, self))

    def __iter__(self):
        return iter((self.latitude, self.longitude))

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return tuple(self) == tuple(other)
        return False

    def __hash__(self):
        return hash(tuple(self))

    def __getitem__(self, index):
        return tuple(self)[index]
