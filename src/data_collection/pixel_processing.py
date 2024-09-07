import os
from dataclasses import dataclass, asdict

from common.logger import logger
from datetime import datetime
from PIL import Image
from time import time
import json

start_time = time()  # script start time
start_datetime = datetime.now()


if not os.path.exists("processed_traffic_images"):
    os.makedirs("processed_traffic_images")


def get_file_last_modified_date(file_path):
    """Helper function to get the timestamp of the scrapped image"""
    timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp)


@dataclass
class TrafficTile:
    lat: float
    lng: float
    traffic_level: float  # Number between 0.0 and 10.0
    src_image_path: str
    image_time: datetime  # comes from the images last modified time since it was created at time of capture

    def as_json(self):
        data = asdict(self)
        data["image_time"] = self.image_time.isoformat()
        return data


def process_pixels(route_name):
    route_path = f"processed_traffic_images/{route_name}"
    if not os.path.exists(route_path):
        os.makedirs(route_path)

    route_tiles = []

    # crop to 10x10 size (around the center) for 360 by 800 (smallest common viewport) screencapture
    # crop image X pixels from direction
    left = 175
    top = 395
    right = 185
    bottom = 405

    logger.info(f"New Run of pixel_processing.py @ {start_datetime}\n")
    # Load the target_coordinates.json file
    with open(f"{route_name}_coordinates.json") as file:
        data = json.load(file)

    # iterate through the captured images based on file name output by serversideimagescrape.js
    for i, coordinate in enumerate(data):
        lat = coordinate["lat"]
        lng = coordinate["lng"]
        logger.info(f"point {i+1} === Lat {lat}, Lng {lng}")
        src_image_path = f"raw_traffic_images/{route_name}_{lat}_{lng}.png"
        picture = Image.open(src_image_path)
        capture_time = get_file_last_modified_date(src_image_path)
        logger.info(f"Image captured: {capture_time}")
        picture = picture.crop((left, top, right, bottom))
        width, height = picture.size
        # logger.info(f"width: {width}, height: {height}")
        picture.save(f"{route_path}/{i+1}_{lat}_{lng}.png")
        green_pix_count = 0
        yellow_pix_count = 0
        red_pix_count = 0
        dark_red_pix_count = 0
        for x in range(width):
            for y in range(height):
                current_color = picture.getpixel((x, y))
                if current_color == (22, 224, 152):
                    green_pix_count += 1
                    logger.info(f"Green pixel at x: {x}, y: {y}")
                elif current_color == (255, 207, 67):
                    yellow_pix_count += 1
                    logger.info(f"Yellow pixel at x: {x}, y: {y}")
                elif current_color == (242, 78, 66):
                    red_pix_count += 1
                    logger.info(f"Red pixel at x: {x}, y: {y}")
                elif current_color == (169, 39, 39):
                    dark_red_pix_count += 1
                    logger.info(f"Dark Red pixel at x: {x}, y: {y}")
        logger.info(f"\033[32mGreen pixel count: {green_pix_count}\033[0m")
        logger.info(f"\033[33mYellow pixel count: {yellow_pix_count}\033[0m")
        logger.info(f"\033[96mRed pixel count: {red_pix_count}\033[0m")
        logger.info(f"\033[90mDark Red pixel count: {dark_red_pix_count}\033[0m")
        all_color_pix_count = (
            green_pix_count + yellow_pix_count + red_pix_count + dark_red_pix_count
        )
        logger.info(f"All traffic pixel count: {all_color_pix_count}")
        warning_count = 0
        if all_color_pix_count == 0:
            logger.warn(
                f"{warning_count}: No primary traffic color pixels found in the image at: {src_image_path}"
            )
            logger.warn(f"{warning_count}: @ time: {datetime.now()}")
            input("Press any key to continue...")
            continue
        traffic_level = (
            green_pix_count * 0
            + yellow_pix_count * 2
            + red_pix_count * 5
            + dark_red_pix_count * 10
        ) / all_color_pix_count
        traffic_tile = TrafficTile(
            float(lat),
            float(lng),
            traffic_level,
            src_image_path,
            capture_time,
        )
        logger.info(f"Traffic Level (0-10): {traffic_level}")
        route_tiles.append(traffic_tile)
    logger.info(
        f"\033[32mRun of pixel_processing.py started @ {start_datetime} has completed\033[0m"
    )
    # report status of the route_tiles
    logger.info(
        f"** {route_name}'s route_tiles is now populated with TrafficTile objects derived from the input images **"
    )

    ### timer for the script
    end_time = time()
    run_time = end_time - start_time
    logger.info(f"\033[34mpixel_processing.py Run time: {run_time} seconds\033[0m")
    logger.info(
        f"\033[32mRun of pixel_processing.py started @ {start_datetime} has completed\033[0m"
    )

    return route_tiles


if __name__ == "__main__":
    route_name = "TEST_CONFIG_TEST"
    route_tiles = process_pixels(route_name)
    route_tiles_raw = [tile.as_json() for tile in route_tiles]
    with open(f"{route_name}.json", "w") as f:
        json.dump(route_tiles_raw, f, indent=2)
