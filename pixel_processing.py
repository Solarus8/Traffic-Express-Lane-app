import os
from datetime import datetime
from PIL import Image
from time import time
import json
start_time = time()  #script start time

###Helper function to get the timestamp of the scrapped image
def get_file_last_modified_date(file_path):
    timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp)

###TrafficTile class = primary data structure for storing the traffic level (10x10 px) tile centeded on the lat, lng coordinates
class TrafficTile:
    def __init__(self, lat, lng, traffic_level, src_image_path, capture_time):
        self.lat = lat
        self.lng = lng
        self.traffic_level = traffic_level
        self.src_image_path = src_image_path
        self.image_time = capture_time  # comes from the images last modified time since it was created at time of catpture

route_name = "US_36_WB"
route_tiles_collection = {}  #collection of TrafficTile objects

#crop to 10x10 size (around the center) for 360 by 800 (smallest common viewport) screencapture
left = 175  #go in X pixels from the left to start croped image
top = 395  #go in X pixels from the Top to start croped image
right = 185 #go in X pixels from the left to stop the croped image (image right side)
bottom = 405 #go in X pixels from the top to stop the croped image (image bottom side)

with open("Log - images with no traffic colors.txt", "a") as log_file:

    # Load the target_coordinates.json file
    with open(f"{route_name}_coordinates.json") as file:
        data = json.load(file)
        #iterate through the captured images based on file name output by serversideimagescrape.js
        #images must be in the same directory as this script
        for i in range(len(data)):
            print(f"point {i+1} === Lat {data[i]['lat']}, Lng {data[i]['lng']}")
            src_image_path = f"{route_name}_{data[i]['lat']}_{data[i]['lng']}_16x_360x800.png"
            picture = Image.open(src_image_path)
            capture_time = get_file_last_modified_date(src_image_path)
            print(f"Image captured: {capture_time}")
            picture = picture.crop((left, top, right, bottom))
            width, height = picture.size
            #print(f"width: {width}, height: {height}")
            picture.save(f"{route_name}_point_{i+1}_10x10px_lat_{data[i]['lat']}_lng_{data[i]['lng']}.png")
            green_pix_count = 0
            yellow_pix_count = 0
            red_pix_count = 0
            dark_red_pix_count = 0
            for x in range(width):
                for y in range(height):
                    current_color = picture.getpixel((x, y))
                    if current_color == (22, 224, 152):
                        green_pix_count += 1
                        print(f"Green pixel at x: {x}, y: {y}")
                    elif current_color == (255, 207, 67):
                        yellow_pix_count += 1
                        print(f"Yellow pixel at x: {x}, y: {y}")
                    elif current_color == (242, 78, 66):
                        red_pix_count += 1
                        print(f"Red pixel at x: {x}, y: {y}")
                    elif current_color == (169, 39, 39):
                        dark_red_pix_count += 1
                        print(f"Dark Red pixel at x: {x}, y: {y}")
            print(f"Green pixel count: {green_pix_count}")
            print(f"Yellow pixel count: {yellow_pix_count}")
            print(f"Red pixel count: {red_pix_count}")
            print(f"Dark Red pixel count: {dark_red_pix_count}")
            all_color_pix_count = green_pix_count + yellow_pix_count + red_pix_count + dark_red_pix_count
            print(f"All traffic pixel count: {all_color_pix_count}")
            if all_color_pix_count == 0:
                print(f"WARNING: No primary traffic color pixels found in the image at: {src_image_path}")
                log_file.write(f"WARNING: No color pixels found in the image at: {src_image_path}/n")
                log_file.flush()
                input("Press any key to continue...")
            traffic_level = (green_pix_count * 0 + yellow_pix_count * 2 + red_pix_count * 5 + dark_red_pix_count * 10) / all_color_pix_count
            current_TrafficTile = TrafficTile(data[i]['lat'], data[i]['lng'], traffic_level, src_image_path, capture_time)
            print(f"Traffic Level (0-10): {current_TrafficTile.traffic_level}")
            route_tiles_collection[f"{route_name} point {i+1}"] = current_TrafficTile
            
print(f"** {route_name}'s route_tiles_collection is now populated with TrafficTile objects derived from the inpute images **")

### timer for the script
end_time = time()
run_time = end_time - start_time
print(f"pixel_processing.py Run time: {run_time} seconds")
