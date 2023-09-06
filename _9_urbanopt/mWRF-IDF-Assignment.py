'''
Please process the following data:
Building id = 1, lat = 41.31529750000000, lon = -105.58152500000001,is assigned to WRF#2, grid 74, lat = 41.31533050537109, lon = -105.58161926269531
Building id = 2, lat = 41.31328985009802, lon = -105.58458895073731,is assigned to WRF#2, grid 22, lat = 41.31347656250000, lon = -105.58409118652344
Building id = 3, lat = 41.31521200000000, lon = -105.57892600000000,is assigned to WRF#3, grid 51, lat = 41.31533050537109, lon = -105.57914733886719

into the following format:
id, wrf, grid
1, 2, 74
2, 2, 22
3, 3, 51
'''

source_file = 'source-child-assignment.txt'
target_file = 'target-child-assignment.txt'

with open(source_file, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    line = line.strip()
    line = line.split(',')
    id = line[0].split()[-1]
    wrf = line[3].split('#')[-1].split(',')[0]
    grid = line[4].split()[-1].split(',')[0]
    new_line = ', '.join([id, wrf, grid])
    new_lines.append(new_line)

with open(target_file, 'w') as f:
    for line in new_lines:
        f.write(line + '\n')