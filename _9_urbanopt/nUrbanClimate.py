'''
read text file, to extract urban temperature
'''
import csv
import os,re
import pandas as pd

def readTextfile(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    curUrbanWeather = []
    for line in lines:
        # Child 0 received weather 13.84 (OAT_C), 0.00800 (Abs_Hum kgw/kga)
        if "Child 0 received weather" in line:
            # extract numbers[1]
            regularExpresForNum = r"[-+]?\d*\.\d+|\d+"
            _nums = re.findall(regularExpresForNum, line)
            curUrbanWeather.append(float(_nums[1]))
    return curUrbanWeather
def iterate_file(base,subfolder,filename):
    col = None
    if "tmy3" in filename:
        col = "TMY3"
    else:
        # online.log.energyplus
        # jun30_100mIDFs38_ep_temp
        date = subfolder.split("_")[0]
        _couple = filename.split(".")[0]
        col = date + "_" + _couple

    curUrbanWeather = readTextfile(os.path.join(base,subfolder,filename))
    return col, curUrbanWeather

def construct_df():
    output_csv_file = 'WY_UrbanClimate.csv'
    # Open the CSV file for writing
    with open(output_csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for subfolder in os.listdir(base_path):
            for _file in os.listdir(os.path.join(base_path, subfolder)):
                col, curUrbanWeather = iterate_file(base_path, subfolder, _file)

                # Write the data to the CSV file
                writer.writerow([col] + curUrbanWeather)

base_path = r"C:\Users\wulic\all_Logs"
construct_df()

