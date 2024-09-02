from PIL import Image
from time import time

start_time = time()

picture = Image.open("gmaps 15z 1920 by 1080 TEST 1.png")

#crop the image captured at 1920 by 1080 to remove gmaps UI elements, end image size is 1539 by 729 pixels
left = 192  #go in 192 pixels from the left to start croped image
top = 176  #go in 176 pixels from the Top to start croped image
right = 1731 #go in 1731 pixels from the left to stop the croped image (image right side)
bottom = 905 #go in 905 pixels from the top to stop the croped image (image bottom side)
picture = picture.crop((left, top, right, bottom))

# Get the size of the image
width, height = picture.size

# Define the standard green color
standard_green = (0, 255, 0)

# use sampled green values as keys  (was not working for some reason!!)
sampled_pixels = [(22, 224, 152), (76, 165, 115), (134, 188, 174), (104, 221, 158), (98, 209, 148), (69, 154, 105), (85, 185, 129), (101, 215, 152), (104, 221, 158), (100, 212, 150), (89, 182, 128)]

# Process every pixel  /// CONSIDER looking into Numpy (maybe also ) for faster processing
for x in range(width):
    for y in range(height):
        current_color = picture.getpixel((x, y))
        # Check if the pixel is a shade of green (corse estimation)
        ##if current_color[0] <= 105 and current_color[1] >= 150 and current_color[2] <= 175 and current_color[0]+current_color[2] < 300:
        if current_color in sampled_pixels:
            print(current_color)
        #    new_color = standard_green:
            new_color = standard_green
        else:
        #new_color = black
            new_color = (0, 0, 0)
        picture.putpixel((x, y), new_color)

# Save the modified image
picture.save("png modified_image 1 with CROP test 4.png")
end_time = time()
run_time = end_time - start_time
print(f"Run time: {run_time} seconds")