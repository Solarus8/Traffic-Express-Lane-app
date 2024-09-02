from PIL import Image
import decimal
from decimal import Decimal, getcontext
from time import time
start_time = time()

# Set the precision for the Decimal class
getcontext().prec = 11

class TrafficPixel:
    def __init__(self, lat, lng, pixcolor, traffic_level, ref_center_pixel_latlng, x_index, y_index):
        self.lat = lat
        self.lng = lng
        self.pixcolor = pixcolor
        self.traffic_level = traffic_level
        self.ref_center_pixel_latlng = ref_center_pixel_latlng
        self.x_index = x_index
        self.y_index = y_index

# Get lat and lng from the target URL (pixel at center of image)
### the source_URL will come from JSON created by puppeteer (javascript) URL capture Script
source_URL = "https://www.google.com/maps/@39.9775161,-105.2338109,15z/data=!5m1!1e1?authuser=0&entry=ttu"
reduced_URL = source_URL.lstrip("https://www.google.com/maps/@").rstrip(",15z/data=!5m1!1e1?authuser=0&entry=ttu")
lat, lng = reduced_URL.split(",")
print(f"lat: {lat}, lng: {lng}")
center_pixel_lat = Decimal(lat) #Decimal is used to maintain precision
print(center_pixel_lat)
center_pixel_lng = Decimal(lng)
print(center_pixel_lng)

# center_pixel_ref (source_URL) lat and lng (as tuple) for reference data to know the heritage of each pixel (i.e. what was the target URL lat and lng)  #float is used to have a basic data type to store in a tuple
center_pixel_lat_float = float(lat)
print(center_pixel_lat_float)
center_pixel_lng_float = float(lng)
print(center_pixel_lng_float)
ref_center_pixel_latlng = (center_pixel_lat_float, center_pixel_lng_float)


# Open the image taken from the Google Maps screenshot
picture1 = Image.open("gmaps 15z 1920 by 1080 TEST 1.png")

#crop the image captured at 1920 by 1080 to remove gmaps UI elements, end image size is 1539 by 729 pixels
left = 192  #go in 192 pixels from the left to start croped image
top = 176  #go in 176 pixels from the Top to start croped image
right = 1731 #go in 1731 pixels from the left to stop the croped image (image right side)
bottom = 905 #go in 905 pixels from the top to stop the croped image (image bottom side)
picture1 = picture1.crop((left, top, right, bottom))

# Get the size of the image which should be 1539 by 729 pixels
width, height = picture1.size
###DEBUGING: print("width: {}, height: {}".format(width, height))

# Initialize the matrix1 with TrafficPixel objects
matrix1 = [[TrafficPixel(lat=0.0, lng=0.0, pixcolor=(0, 0, 0), traffic_level=0, ref_center_pixel_latlng=(0,0), x_index=None, y_index=None) for _ in range(height)] for _ in range(width)]
###DEBUGING: print(len(matrix1))
###DEBUGING: print(len(matrix1[0]))

# Process every pixel
for x in range(width):
    for y in range(height):
        matrix1[x][y].x_index = x
        matrix1[x][y].y_index = y
        matrix1[x][y].ref_center_pixel_latlng = ref_center_pixel_latlng
        try:
            matrix1[x][y].lat = center_pixel_lat + Decimal((y + 364) * 0.00003271) # 0.00003271 is the approximate latitude difference per pixel
        except IndexError:
            print("IndexError for x: {}, y: {}".format(x, y))
            break
        matrix1[x][y].lng = center_pixel_lng + Decimal((x - 796) * 0.00004264)  # 0.00004264 is the approximate longitude difference per pixel (at Denver, CO latitude i.e. 39-40° N)
        current_color = picture1.getpixel((x, y))
        matrix1[x][y].pixcolor = current_color
        #print(f"Lat: {matrix1[x][y].lat}, Lng: {matrix1[x][y].lng}, Pixcolor: {matrix1[x][y].pixcolor}, Traffic Level: {matrix1[x][y].traffic_level}, Ref Center Pixel LatLng: {matrix1[x][y].ref_center_pixel_latlng}, Pixel Index: {matrix1[x][y].x_index}, {matrix1[x][y].y_index}")

print(f"pic1 center pic lat is {matrix1[769][364].lat} and lng is {matrix1[0][0].lng}")
# TrafficPixel object at at the top left corner of the image
pic1_top_left_pixel = matrix1[0][0]
print("Top left pixel of picture1 is --")
print(f"Lat: {pic1_top_left_pixel.lat}, Lng: {pic1_top_left_pixel.lng}, Pixcolor: {pic1_top_left_pixel.pixcolor}, Traffic Level: {pic1_top_left_pixel.traffic_level}, Ref Center Pixel LatLng: {pic1_top_left_pixel.ref_center_pixel_latlng}, Pixel Index: x = {pic1_top_left_pixel.x_index}, y = {pic1_top_left_pixel.y_index}")

#picture2 is the image received by passing top left corner pixel lat lng from picture1 as the target center of the image based on pixel caculations for Latitude and Longitude
picture2 = Image.open("gmaps 15z 1920 by 1080 TEST 1 - recenter top left.png")

#crop picture2 image also captured at 1920 by 1080 to remove gmaps UI elements, end image size is 1539 by 729 pixels.  This croping is the same process as used on the first picture1 image.
picture2 = picture2.crop((left, top, right, bottom))

### center point for picture2 is 39.9894388, -105.2666223 which could be simply calculated from the top left corner pixel of picture1 but here it is hardcoded for testing based on what was used in the image capture javascript seversideimagescrape.js
center_pixel_lat2 = Decimal(39.9894388)  #Decimal is used to maintain precision
center_pixel_lng2 = Decimal(-105.2666223)

center_pixel_lat_float2 = float(39.9894388) #float is used to have a basic data type to store in a tuple
center_pixel_lng_float2 = float(-105.2666223)
ref_center_pixel_latlng2 = (center_pixel_lat_float2, center_pixel_lng_float2)

# Get the size of the image which should be 1539 by 729 pixels
width2, height2 = picture2.size

# Initialize matrix2 for picture2 with TrafficPixel objects
matrix2 = [[TrafficPixel(lat=0.0, lng=0.0, pixcolor=(0, 0, 0), traffic_level=0, ref_center_pixel_latlng=(0,0), x_index=None, y_index=None) for _ in range(height2)] for _ in range(width2)]

# Process every pixel of picture2
for x in range(width):
    for y in range(height):
        matrix2[x][y].x_index = x
        matrix2[x][y].y_index = y
        matrix2[x][y].ref_center_pixel_latlng = ref_center_pixel_latlng2
        try:
            matrix2[x][y].lat = center_pixel_lat2 + Decimal((y + 364) * 0.00003271) # 0.00003271 is the approximate latitude difference per pixel
        except IndexError:
            print("IndexError for x: {}, y: {}".format(x, y))
            break
        matrix2[x][y].lng = center_pixel_lng2 + Decimal((x - 796) * 0.00004264)  # 0.00004264 is the approximate longitude difference per pixel (at Denver, CO latitude i.e. 39-40° N)
        current_color = picture2.getpixel((x, y))
        matrix2[x][y].pixcolor = current_color
        #print(f"Lat: {matrix2[x][y].lat}, Lng: {matrix2[x][y].lng}, Pixcolor: {matrix2[x][y].pixcolor}, Traffic Level: {matrix2[x][y].traffic_level}, Ref Center Pixel LatLng: {matrix2[x][y].ref_center_pixel_latlng}")

        # TrafficPixel object at at the top left corner of the image
pic2_top_left_pixel = matrix2[0][0]
print("Top left pixel of picture2 is --")
print(f"Lat: {pic2_top_left_pixel.lat}, Lng: {pic2_top_left_pixel.lng}, Pixcolor: {pic2_top_left_pixel.pixcolor}, Traffic Level: {pic2_top_left_pixel.traffic_level}, Ref Center Pixel LatLng: {pic2_top_left_pixel.ref_center_pixel_latlng}, Pixel Index: y = {pic2_top_left_pixel.x_index}, x = {pic2_top_left_pixel.y_index}")

print(matrix1[0][0].lat)
print(matrix2[1538][728].lat)

# Example output format
print("Comparison complete.")

### timer for the script
end_time = time()
run_time = end_time - start_time
print(f"Run time: {run_time} seconds")