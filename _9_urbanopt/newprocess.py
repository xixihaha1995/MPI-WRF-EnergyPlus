import json
filename = "Wyoming.geojson"
save_file = "UWyo.geojson"
# 41.311782, -105.585284
# 41.314619, -105.577613
lat_down = 41.311200
lat_up = 41.313557
long_left = -105.582037
long_right = -105.577335
# Open the JSON file
with open(filename) as file:
    # Load the JSON data
    data = json.load(file)
# copy data to newdict
newdict = data.copy()
newdict['features'] = []

for item in data['features']:
    # item['geometry']['coordinates'] is a list [[[-104.047716, 41.999261], [-104.04778, 41.999261], [-104.04778, 41.999215], [-104.047716, 41.999215], [-104.047716, 41.999261]]]
    # if any of the coordinates are in the range, then add the item to the newdict
    if any(lat_down < float(substring) < lat_up for substring in item['geometry']['coordinates'][0][0]) and \
            any(long_left < float(lon_substring) < long_right for lon_substring in item['geometry']['coordinates'][0][0]):
        print(item)
        newdict['features'].append(item)

# Save the matching lines to a new file
with open(save_file, 'w') as file:
    json.dump(newdict, file)