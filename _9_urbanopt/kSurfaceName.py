'''
This script is used to process surface names.

Source file has the following format:
id;right(bot,mid,mid,top);left(bot,mid,mid,top);up(bot,mid,mid,top);down(bot,mid,mid,top);roof
7;24,82,140,198;36,94,152,210;54,112,170,228;30,88,146,204;184;

Target file has the following format:
id; bot; midcount;mid; top;roof;
1; 8, 20, 26, 14;8;38, 50, 56, 44, 68, 80, 86, 74;98, 110, 116, 104;96;

Directions:
1. keep id and roof unchanged
2. reorganize `right, left, up, down` to `bot, midcount, mid, top`
'''
import os

# source file
source_file = r'C:\Users\wulic\Documents\GitHub\fortran_experiments\_10Cheyenne\h38IDFs\resources-23-1-0\surfaceNamesRLUD.txt'
# target file
target_file = r'C:\Users\wulic\Documents\GitHub\fortran_experiments\_10Cheyenne\h38IDFs\resources-23-1-0\surfaceNamesBMT.txt'

# read source file
with open(source_file, 'r') as f:
    lines = f.readlines()

# process lines
new_lines = []
for line in lines:
    # split line
    line = line.strip()
    line = line.split(';')
    # keep id and roof unchanged
    id = line[0]
    roof = line[-2]
    bot = []
    midcount = 8
    mid = [0] * midcount
    top = []
    # reorganize `right, left, up, down` to `bot, midcount, mid, top`
    for i in range(1, 5):
        # split `right, left, up, down`
        temp = line[i].split(',')
        # get bot, midcount, mid, top
        bot.append(temp[0])
        mid[i-1] = temp[1]
        mid[i+3] = temp[2]
        top.append(temp[3])
    # join bot, mid, top
    bot = ', '.join(bot)
    mid = ', '.join(mid)
    top = ', '.join(top)
    # join line
    new_line = '; '.join([id, bot, str(midcount), mid, top, roof])
    # add ';' to the end of the line
    new_line = new_line + ';'
    new_lines.append(new_line)

# write target file
with open(target_file, 'w') as f:
    for line in new_lines:
        f.write(line + '\n')
        