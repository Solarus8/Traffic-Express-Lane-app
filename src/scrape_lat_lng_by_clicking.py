from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import json

from logger import logger
from target_config import target_route

###
###*** CONFIGUATION - TARGET ROUTE NAME in config.py ***###
###

# Set up the WebDriver (assuming ChromeDriver is in the PATH)
driver = webdriver.Chrome()

# Input the starting latitude and longitude values for the start of the route
driver.get("https://epsg.io/map#srs=4326&x=-104.990333&y=39.827730&z=16&layer=streets")

# JavaScript to add an event listener for clicks on the map
js_script = """
document.getElementById('map').addEventListener('click', function() {
    window.location.hash = window.location.hash; // Trigger URL change
});
"""
driver.execute_script(js_script)  # Execute the JavaScript to add the event listener

# List to store the coordinates (Key:Value) to be written to a JSON file
coord_list = []

# Open a log file to write the URLs
with open("../url_log.txt", "a") as log_file:
    logger.info("Starting Scraping log...")
    log_file.write(f"*****Starting Scraping log...")
    log_file.flush()
    try:
        while True:

            # Wait for the URL to change
            WebDriverWait(driver, 180).until(EC.url_changes(driver.current_url))

            # Get the current URL
            current_url = driver.current_url

            # Parse the URL to extract latitude and longitude
            parsed_url = urllib.parse.urlparse(current_url)
            query_params = urllib.parse.parse_qs(parsed_url.fragment)

            if "x" in query_params and "y" in query_params:
                longitude = query_params["x"][0]
                latitude = query_params["y"][0]

                # Log the URL and coordinates to log file
                log_file.write(
                    f"{current_url}\nLatitude: {latitude}, Longitude: {longitude}\n"
                )
                log_file.flush()

                # Append the current latitude and longitude to the list of coordinates
                current_latlng_dict = {"lat": latitude, "lng": longitude}
                coord_list.append(current_latlng_dict)

                # Print the URL and coordinates to the console
                logger.info(f"Logged URL: {current_url}")
                logger.info(f"Latitude: {latitude}, Longitude: {longitude}")
            # except selenium.common.exceptions.TimeoutException: # type: ignore
            #    logger.info("Timeout waiting for URL to change. Retrying...")
    except KeyboardInterrupt:
        logger.info("Stopped logging on KeyboardInterrupt!")
    finally:
        # Write the list of coordinates to a JSON file
        with open(f"{target_route}_coordinates.json", "w") as json_file:
            json.dump(coord_list, json_file, indent=4)
        # Close the WebDriver
        driver.quit()
    log_file.write(f"Stopped logging.*****\n")
    log_file.flush()
