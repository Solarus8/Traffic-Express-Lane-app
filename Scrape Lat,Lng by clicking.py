from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import json

# Set up the WebDriver (assuming ChromeDriver is in the PATH)
driver = webdriver.Chrome()

# Navigate to the target website
driver.get("https://epsg.io/map#srs=4326&x=-105.144632&y=39.944243&z=16&layer=streets")

# JavaScript to add an event listener for clicks on the map
js_script = """
document.getElementById('map').addEventListener('click', function() {
    window.location.hash = window.location.hash; // Trigger URL change
});
"""

# Execute the JavaScript to add the event listener
driver.execute_script(js_script)

# List to store the coordinate strings to be written to a JSON file
coord_list = []

# Open a log file to write the URLs
with open("url_log.txt", "a") as log_file:
    try:
        while True:
            try:
                # Wait for the URL to change
                WebDriverWait(driver, 60).until(EC.url_changes(driver.current_url))
            
                # Get the current URL
                current_url = driver.current_url
            
                # Parse the URL to extract latitude and longitude
                parsed_url = urllib.parse.urlparse(current_url)
                query_params = urllib.parse.parse_qs(parsed_url.fragment)
            
                if 'x' in query_params and 'y' in query_params:
                    longitude = query_params['x'][0]
                    latitude = query_params['y'][0]
                    
                    # Log the URL and coordinates to log file
                    log_file.write(f"{current_url}\nLatitude: {latitude}, Longitude: {longitude}\n")
                    log_file.flush()

                    # Append the current latitude and longitude to the list of coordinates
                    current_latlng_dict = {"lat": latitude, "lng": longitude}
                    coord_list.append(current_latlng_dict)

                    # Print the URL and coordinates to the console
                    print(f"Logged URL: {current_url}")
                    print(f"Latitude: {latitude}, Longitude: {longitude}")
            except selenium.common.exceptions.TimeoutException: # type: ignore
                print("Timeout waiting for URL to change. Retrying...")
    except KeyboardInterrupt: 
        print("Stopped logging.")
    finally:
        # Write the list of coordinates to a JSON file
        with open("target_coordinates.json", "w") as json_file:
            json.dump(coord_list, json_file, indent=4)
        # Close the WebDriver
        driver.quit()
 