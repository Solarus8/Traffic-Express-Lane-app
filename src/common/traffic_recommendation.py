from common.gate import Gate
from common.custom_types import Coordinate
from common.express_lane import ExpressLane
from data_collection.traffic_data import get_traffic_rating, get_duration_in_traffic


def recommend(
    gate_name, sensitivity: float = 1.5
) -> (bool, None | float, None | ExpressLane, str):
    """Find out if an express lane will be recommended for the given coordinates"""
    gate = Gate.by_name(gate_name)
    if not gate:
        return False, None, None, "No gate found"
    # ToDo: add case if express lane is closed
    express_lane = gate.express_lane
    duration, duration_in_traffic = get_duration_in_traffic(
        express_lane.start_coordinate, express_lane.end_coordinate
    )
    rating = get_traffic_rating(
        express_lane.start_coordinate, express_lane.end_coordinate
    )
    # If it takes 1.5 times longer than usual because of traffic, recommend
    estimated_time_saving = duration_in_traffic - duration
    if rating > sensitivity:
        return True, estimated_time_saving, express_lane, "Recommended"
    return False, estimated_time_saving, express_lane, "Not recommended"


if __name__ == "__main__":
    current_coordinate = Coordinate(39.834298, -105.0189317)
    print("Recommends taking express lane:", recommend(current_coordinate))
