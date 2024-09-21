import pytest
import json
from unittest.mock import patch
from fastapi.testclient import TestClient
from common.custom_types import Coordinate
from common.express_lane import ExpressLane
from common.traffic_recommendation import recommend
from run_api import app  # Adjust this import according to your actual module path


client = TestClient(app)


def test_ws_recommend():
    # Mock dependencies
    with patch("common.traffic_recommendation.recommend") as mock_recommend:
        # Create a mock ExpressLane object
        mock_lane = ExpressLane(
            name="Mock Lane",
            start_coordinate=Coordinate(39.834298, -105.0189317),
            end_coordinate=Coordinate(39.900000, -105.000000),
            route="Mock Route",
        )
        mock_recommend.return_value = mock_lane

        # Connect to WebSocket
        with client.websocket_connect("/api/recommend?user_id=123") as websocket:
            # Send data in JSON format
            websocket.send_json(
                {
                    "coordinates": "39.834298,-105.0189317",
                    "timestamp": 1726931872.528192,
                }
            )

            # Receive response
            response = websocket.receive_text()
            lane_data = json.loads(response)

            # Assertions
            assert lane_data["name"] == "Mock Lane"
            assert lane_data["route"] == "Mock Route"
            assert lane_data["start_coordinate"]["latitude"] == 39.834298
            assert lane_data["start_coordinate"]["longitude"] == -105.0189317


def test_ws_recommend_no_lane():
    # Mock dependencies
    with patch("common.traffic_recommendation.recommend") as mock_recommend:
        mock_recommend.return_value = None  # Simulate no lane recommendation

        # Connect to WebSocket
        with client.websocket_connect("/api/recommend?user_id=123") as websocket:
            # Send data in JSON format
            websocket.send_json(
                {
                    "coordinates": "39.834298,-105.0189317",
                    "timestamp": 1726931872.528192,
                }
            )

            # Receive response
            response = websocket.receive_text()

            # Assertions
            assert response == "None"
