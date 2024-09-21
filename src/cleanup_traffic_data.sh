#!/bin/bash

# Directory to check
DIR="traffic_data"

# Loop to run every 30 seconds
while true; do
    # Find and delete files older than 5 minutes
    find "$DIR" -type f -mmin +5 -exec rm {} \;

    # Wait for 30 seconds
    sleep 30
done
