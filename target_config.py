import json
#This defines the variable for the target route to be used in the other py files
target_route = "TEST_CONFIG_TEST"  # RUN THIS FILE AFTER UPDATING THIS VARIABLE
# "target_config.json" is used to pass the target route to the javascript files

# Write the target_route to a JSON file for use in javascript files
with open('target_config.json', 'w') as json_file:
    json.dump({'target_route': target_route}, json_file)