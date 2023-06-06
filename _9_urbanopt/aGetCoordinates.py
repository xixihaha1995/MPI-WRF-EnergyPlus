import json
filename = "Wyoming.geojson"
save_file = "UWyo.geojson"
# small area: 41.311200, -105.582037, 41.313557, -105.577335
# large area: 41.291737, -105.623253, 41.335317, -105.542058
# 1km: 41.311629, -105.585654, 41.315433, -105.570806
lat_down = 41.311629
lat_up = 41.315433
long_left = -105.585654
long_right = -105.570806
# Open the JSON file
with open(filename) as file:
    # Load the JSON data
    data = json.load(file)
# copy data to newdict
newdict = data.copy()
newdict['features'] = []
count = 0
for item in data['features']:
    # item['geometry']['coordinates'] is a list [[[-104.047716, 41.999261], [-104.04778, 41.999261], [-104.04778, 41.999215], [-104.047716, 41.999215], [-104.047716, 41.999261]]]
    # if any of the coordinates are in the range, then add the item to the newdict
    if any(lat_down < float(substring) < lat_up for substring in item['geometry']['coordinates'][0][0]) and \
            any(long_left < float(lon_substring) < long_right for lon_substring in item['geometry']['coordinates'][0][0]):
        print(item)
        count += 1
        # newdict['features'].append(item)
print(count)
# # Save the matching lines to a new file
# with open(save_file, 'w') as file:
#     json.dump(newdict, file)