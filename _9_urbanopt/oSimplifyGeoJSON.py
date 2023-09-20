import json

sourceFile = 'buildings_urbanopt_uwyo.json'
targetFile = 'buildings_urbanopt_uwyo_simplified.json'

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
        coords = feature['geometry']['coordinates'][0]
        x = [coord[0] for coord in coords]
        y = [coord[1] for coord in coords]
        xMin = min(x)
        xMax = max(x)
        yMin = min(y)
        yMax = max(y)
        feature['geometry']['coordinates'] = [[[xMin, yMin], [xMax, yMin], [xMax, yMax], [xMin, yMax], [xMin, yMin]]]

        feature['properties']['number_of_stories'] = 3
        feature['properties']['floor_area'] = feature['properties']['number_of_stories']  \
                                              * feature['properties']['footprint_area']



with open(targetFile, 'w') as f:
    json.dump(data, f, indent=4)
