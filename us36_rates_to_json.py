import csv
import json

toll_rates_file = "Other Docs/express lane rates/US36_rates/US36 EB express lane rates.csv"
toll_liscence_rates_file = "Other Docs/express lane rates/US36_rates/US36 EB License express lane rates.csv"
express_lanes_file = "src/resources/US36 EB express lane start and end points.csv"


lanes = {}


with open(toll_rates_file) as f:
    reader = csv.reader(f)
    # Skip two header rows
    next(reader)
    next(reader)
    for row in reader:
        if row[0] == "":
            # Empty row reached, no more interesting information after that
            break
        elif row[0] == "Time of Day":
            express_lane_names = row[1:]
            for lane_name in express_lane_names:
                lanes[lane_name] = {
                    "lane_name": lane_name,
                    "road_name": "US36",
                    "direction": "EB",
                    "lines_start": {},
                    "lines_end": {},
                    "effective_start": {},
                    "effective_end": {},
                    "lines_length": 0,
                    "effective_length": 0,
                    "hours_tolls": {},
                    "hours_license_tolls": {}
                }
        else:
            tod, *express_lane_rates = row
            for i, rate in enumerate(express_lane_rates):
                lane_name = express_lane_names[i]
                lane = lanes[lane_name]
                lane["hours_tolls"][tod] = rate

with open(toll_liscence_rates_file) as f:
    reader = csv.reader(f)
    # Skip three header rows
    next(reader)
    next(reader)
    next(reader)
    for row in reader:
        if row[0] == "":
            # Empty row reached, no more interesting information after that
            break
        else:
            tod, *express_lane_liscence_rates = row
            for i, rate in enumerate(express_lane_liscence_rates):
                lane_name = express_lane_names[i]
                lane = lanes[lane_name]
                lane["hours_license_tolls"][tod] = rate

with open(express_lanes_file) as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if row[0] == "":
            # Empty row reached, no more interesting information after that
            break
        else: 
            start_lat, start_lng,end_lat, end_lng, eff_start_lat, eff_start_lng, eff_end_lat, eff_end_lng, name, *_ = row
            if name in lanes:
                lane = lanes[name]
                lane["lines_start"]["latitude"] = start_lat
                lane["lines_start"]["longitude"] = start_lng
                lane["lines_end"]["latitude"] = end_lat
                lane["lines_end"]["longitude"] = end_lng
                lane["effective_start"]["latitude"] = eff_start_lat
                lane["effective_start"]["longitude"] = eff_start_lng
                lane["effective_end"]["latitude"] = eff_end_lat
                lane["effective_end"]["longitude"] = eff_end_lng

result = list(lanes.values())

print(json.dumps(result, indent=2))
