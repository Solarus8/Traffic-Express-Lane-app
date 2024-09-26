import json
import csv
import os

# Absolute path to the JSON file
json_file_path = r'c:\Code HQ\Traffic Express Lane app\src\resources\travelPathtest.json'

# Step 1: Read the JSON file
try:
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Failed to decode JSON - {e}")
    exit(1)

# Step 2: Extract latitude and longitude
coordinates = []
for entry in data:
    coords = entry.get('coords', {})
    latitude = coords.get('latitude')
    longitude = coords.get('longitude')
    if latitude is not None and longitude is not None:
        coordinates.append({'latitude': latitude, 'longitude': longitude})
    else:
        print(f"Warning: Missing latitude or longitude in entry: {entry}")

# Step 3: Write to CSV
try:
    with open('output.csv', 'w', newline='') as csv_file:
        fieldnames = ['latitude', 'longitude']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(coordinates)
    print("CSV file 'output.csv' created successfully.")
except IOError as e:
    print(f"Error: Failed to write to CSV file - {e}")