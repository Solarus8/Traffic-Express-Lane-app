from common.checkpoint import Checkpoint
from common.custom_types import Coordinate
from common.express_lane import ExpressLane
from data_collection.traffic_data import get_traffic_rating


def recommend(
    coordinates: Coordinate, sensitivity: float = 1.5
) -> (None | bool, ExpressLane):
    """Find out if an express lane will be recommended for the given coordinates"""
    checkpoint = Checkpoint.from_coordinate(coordinates)
    if not checkpoint:
        return
    express_lane = checkpoint.express_lane
    rating = get_traffic_rating(
        express_lane.start_coordinate, express_lane.end_coordinate
    )
    print("Rating:", rating)
    # If it takes 1.5 times longer than usual because of traffic, recommend
    if rating > sensitivity:
        return True, express_lane
    return False, express_lane


if __name__ == "__main__":
    current_coordinate = Coordinate(39.834298, -105.0189317)
    print("Recommends taking express lane:", recommend(current_coordinate))
