import json

filename = "Wyoming.geojson"
target_string = "-105.57"
output_file = "UWyo.geojson"
filtered_lines = []

# Open the GeoJSON file for reading
with open(filename, 'r') as file:
    lines = file.readlines()

# Count the lines containing "-105.57" and save them to a list
# matching_lines = [line for line in lines if any(substring in line for substring in [ '41.312', '41.413', '41.314', '41.315']) and any(lon_substring in line for lon_substring in ['-105.577', '-105.578', '-105.579', '-105.580', '-105.581', '-105.582', '-105.583', '-105.584'])]
# matching_lines = [line for line in lines if any(41.312 < float(substring) < 41.315 for substring in line.split()) and any(-105.584 < float(lon_substring) < -105.577 for lon_substring in line.split())]
matching_lines = []
lat_down = 41.312
lat_up = 41.315
long_left = -105.584
long_right = -105.577

for line in lines:
    lat_condition = any(
        lat_down < float(substring) < lat_up for substring in line.split() if substring.replace('.', '', 1).isdigit())
    long_condition = any(long_left < float(lon_substring) < long_right for lon_substring in line.split() if
                         lon_substring.replace('.', '', 1).isdigit())

    if lat_condition and long_condition:
        matching_lines.append(line)

# Count the number of matching lines
count = len(matching_lines)

# Save the matching lines to a new file
with open(output_file, 'w') as file:
    file.writelines(matching_lines)

# Print the count
print(f"Number of lines containing '-105.57': {count}")


