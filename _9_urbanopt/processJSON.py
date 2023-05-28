import json

filename = "Wyoming.geojson"
target_string = "-105.57"
output_file = "UWyo.geojson"
filtered_lines = []

# Open the GeoJSON file for reading
with open(filename, 'r') as file:
    lines = file.readlines()

# Count the lines containing "-105.57" and save them to a list
matching_lines = [line for line in lines if any(substring in line for substring in [ '41.312', '41.413', '41.314', '41.315']) and any(lon_substring in line for lon_substring in ['-105.577', '-105.578', '-105.579', '-105.580', '-105.581', '-105.582', '-105.583', '-105.584'])]

# Count the number of matching lines
count = len(matching_lines)

# Save the matching lines to a new file
with open(output_file, 'w') as file:
    file.writelines(matching_lines)

# Print the count
print(f"Number of lines containing '-105.57': {count}")


