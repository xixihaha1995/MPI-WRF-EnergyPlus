'''
I have one building geoJSON file "buildings_urbanopt_uwyo.json".
Please iterate through its features, and generate one centroid.txt file for all the buildings.
You might want to refer to the following code snippet:
for idx in [1,39]
    data['features'][idx]['geometry']['coordinates']
'''
import json
from shapely.geometry import Polygon
import os, sys

input_file = "buildings_urbanopt_uwyo.json"
output_file = "centroid.csv"
nbrbld = 38

# Open the JSON file
with open(input_file) as file:
    # Load the JSON data
    data = json.load(file)

# create a new file
f = open(output_file, "w")

# write the header
f.write("id, lat, long\n")

# iterate through the features
for idx in range(1, nbrbld+1):
    # get the coordinates
    coordinates = data['features'][idx]['geometry']['coordinates'][0]
    # create a polygon
    polygon = Polygon(coordinates)
    # get the centroid
    centroid = polygon.centroid
    # write the data to the file
    f.write(f"{idx}, {centroid.y}, {centroid.x}\n")

# close the file
f.close()
