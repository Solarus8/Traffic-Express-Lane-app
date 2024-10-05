import json
from datetime import timedelta, datetime, timezone

from starlette.websockets import WebSocket

from common.custom_types import Coordinate
from common.logger import logger
from common.traffic_recommendation import recommend


class CommunicationManager:
    def __init__(self, ws: WebSocket, user_id):
        self.ws = ws
        self.user_id = user_id
        self.last_message = None
        self.coordinate = None
        self.method_order = [
            self.check_express_lane_recommendation,
        ]

    async def update(self):
        data = await self.ws.receive_json()
        client_datetime = datetime.fromtimestamp(data["timestamp"], timezone.utc)
        server_datetime = datetime.now(timezone.utc)
        time_diff = server_datetime - client_datetime
        if time_diff > timedelta(milliseconds=200):
            logger.warning(
                f"Client {self.user_id}'s timestamp is {time_diff.total_seconds()} seconds before server's"
            )

        coordinate = Coordinate(data["latitude"], data["longitude"])
        logger.debug(f"Received coordinate: `{coordinate}`")

        self.coordinate = coordinate
        for method in self.method_order:
            text = await method()
            if text and text != self.last_message:
                self.last_message = text
                await self.ws.send_text(text)
                break

            self.last_message = None

    async def check_express_lane_recommendation(self) -> None | str:
        """Find out if an express lane will be recommended for the given coordinates"""
        do_recommend, lane = recommend(self.coordinate)
        if lane:
            data = lane.as_json()
            data["recommend"] = do_recommend
            text = json.dumps(data)
            logger.debug("Lane recommended:", lane)
            return text
