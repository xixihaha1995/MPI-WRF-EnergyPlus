'''
I need to create one GeoJSON file, with geometry and non-geometry data, for each building.
1. The geometry data is the coordinates of the building. file name: coordinates_uwyo.json
2. The template for the final GeoJSON file (including geometry and non-geometry data, and two sample building)
    is the file: template_urbanopt_uwyo.geojson
3. This script will feed all the coordinates of the buildings into the template, and create a new GeoJSON file,
named: buildings_urbanopt_uwyo.geojson
'''
import json
from shapely.geometry import Polygon
from pyproj import Geod
coordinates_file = "coordinates_uwyo.json"
template_file = "template_urbanopt_uwyo.json"
save_file = "buildings_urbanopt_uwyo.json"
# Open the JSON file
with open(coordinates_file) as file:
    # Load the JSON data
    coor_data = json.load(file)
# Open the JSON file
with open(template_file) as file:
    # Load the JSON data
    to_save_data = json.load(file)
pass

# to_save_data['features'] is a list,
# each item is a dictionary, to_save_data['features'][0] is different from others, its coordinates is a point.
# others are polygons.

def generate_bld(id, coordinates):
    sample_bld = {}
    sample_bld['type'] = 'Feature'
    sample_bld['properties'] = {}
    sample_bld['properties']['id'] = str(id)
    sample_bld['properties']['name'] = f'bld_{id}'
    sample_bld['properties']['type'] = 'Building'
    sample_bld['properties']['number_of_stories'] = 4

    polygon = Polygon(coordinates[0])
    geod = Geod(ellps='WGS84')
    poly_area_m2, poly_perimeter_m = geod.geometry_area_perimeter(polygon)
    poly_area_ft2 = poly_area_m2 * 10.7639
    sample_bld['properties']['footprint_area'] = poly_area_ft2

    sample_bld['properties']['floor_area'] = \
        sample_bld['properties']['number_of_stories'] \
        * sample_bld['properties']['footprint_area']
    sample_bld['properties']['building_type'] = "Mixed use"
    sample_bld['properties']['mixed_type_1'] = "Office"
    sample_bld['properties']['mixed_type_1_percentage'] = 40
    sample_bld['properties']['mixed_type_2'] = "Education"
    sample_bld['properties']['mixed_type_2_percentage'] = 60
    sample_bld['geometry'] = {}
    sample_bld['geometry']['type'] = 'Polygon'
    sample_bld['geometry']['coordinates'] = coordinates
    return sample_bld

count_bld = 1
# only keep to_save_data['features'][0]
to_save_data['features'] = [to_save_data['features'][0]]
for item in coor_data['features']:
    coordinates = item['geometry']['coordinates']
    to_save_data['features'].append(generate_bld(count_bld, coordinates))
    count_bld += 1

# Save the matching lines to a new file
with open(save_file, 'w') as file:
    json.dump(to_save_data, file)
