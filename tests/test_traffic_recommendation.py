import pytest
from unittest.mock import patch, Mock
from common.custom_types import Coordinate
from common.express_lane import ExpressLane
from common import traffic_recommendation
from common.traffic_recommendation import recommend


@pytest.fixture
def mock_express_lane():
    """Fixture to create a mock express lane."""
    return ExpressLane(
        name="Test Express Lane",
        start_coordinate=Coordinate(39.834298, -105.0189317),
        end_coordinate=Coordinate(39.900000, -105.000000),
        route="Test Route",
    )


@pytest.fixture
def mock_checkpoint(mock_express_lane):
    """Fixture to create a mock checkpoint."""
    mock_cp = Mock()
    mock_cp.express_lane = mock_express_lane
    mock_cp.contains_coordinate.return_value = True
    return mock_cp


@patch("common.traffic_recommendation.Checkpoint.from_coordinate")
@patch("common.traffic_recommendation.get_traffic_rating")
def test_recommend_express_lane(
    mock_get_traffic_rating, mock_from_coordinate, mock_checkpoint
):
    # Set up mock return values
    mock_from_coordinate.return_value = mock_checkpoint
    mock_get_traffic_rating.return_value = (
        2.0  # Higher than 1.5 to trigger recommendation
    )

    # Test with a specific coordinate
    coordinate = Coordinate(39.834298, -105.0189317)
    recommended_lane = recommend(coordinate)

    # Assertions
    assert recommended_lane is not None
    assert recommended_lane.name == "Test Express Lane"
    mock_get_traffic_rating.assert_called_once_with(
        mock_checkpoint.express_lane.start_coordinate,
        mock_checkpoint.express_lane.end_coordinate,
    )


@patch("common.traffic_recommendation.Checkpoint.from_coordinate")
@patch("common.traffic_recommendation.get_traffic_rating")
def test_no_recommendation_for_low_traffic(
    mock_get_traffic_rating, mock_from_coordinate, mock_checkpoint
):
    # Set up mock return values
    mock_from_coordinate.return_value = mock_checkpoint
    mock_get_traffic_rating.return_value = 1.0  # Lower than 1.5, so no recommendation

    # Test with a specific coordinate
    coordinate = Coordinate(39.834298, -105.0189317)
    recommended_lane = recommend(coordinate)

    # Assertions
    assert recommended_lane is None
    mock_get_traffic_rating.assert_called_once_with(
        mock_checkpoint.express_lane.start_coordinate,
        mock_checkpoint.express_lane.end_coordinate,
    )


@patch("common.traffic_recommendation.Checkpoint.from_coordinate")
def test_no_checkpoint_found(mock_from_coordinate):
    # Set up mock return values
    mock_from_coordinate.return_value = None  # No checkpoint found

    # Test with a specific coordinate
    coordinate = Coordinate(39.834298, -105.0189317)
    recommended_lane = recommend(coordinate)

    # Assertions
    assert recommended_lane is None
    mock_from_coordinate.assert_called_once_with(coordinate)
