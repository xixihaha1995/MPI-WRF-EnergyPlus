import json
from shapely.geometry import Polygon
sourceFile = 'buildings_urbanopt_uwyo.json'
targetFile = 'buildings_urbanopt_uwyo_simplified.json'
_centroidOutput = 'WY-Simplified-Centroids.csv'
_ftprintm2lst = []

f_centroid = open(_centroidOutput, "w")
f_centroid.write("id, lat, long\n")
'''
There are features in the GeoJSON file that has geometry type of "Polygon".
Please do a min max for its coordinates and convert those multiple vertices 
into a rectangle with 4 vertices.
'''

with open(sourceFile) as f:
    data = json.load(f)
    features = data['features']

for feature in features:
    if feature['geometry']['type'] == 'Polygon':
        # coords = feature['geometry']['coordinates'][0]
        # x = [coord[0] for coord in coords]
        # y = [coord[1] for coord in coords]
        # xMin = min(x)
        # xMax = max(x)
        # yMin = min(y)
        # yMax = max(y)
        # feature['geometry']['coordinates'] = [[[xMin, yMin], [xMax, yMin], [xMax, yMax], [xMin, yMax], [xMin, yMin]]]
        # #lat, long to square meters
        polygon = Polygon(feature['geometry']['coordinates'][0])
        ft_print_m2 = polygon.area * 1e10
        centroid = polygon.centroid
        ft_print_ft2 = ft_print_m2 * 10.7639
        feature['properties']['footprint_area'] = ft_print_ft2
        feature['properties']['number_of_stories'] = 3
        feature['properties']['floor_area'] = feature['properties']['number_of_stories']  \
                                              * feature['properties']['footprint_area']
        # format ft_print_m2 to 2 decimal places
        _ftprintm2lst.append(round(ft_print_m2, 2))
        # write the data to the file
        f_centroid.write(f"{feature['properties']['id']}, {centroid.y}, {centroid.x}\n")

print(f"All IDFs footprint area()m2: {_ftprintm2lst}")
f_centroid.close()
with open(targetFile, 'w') as f:
    json.dump(data, f, indent=4)
