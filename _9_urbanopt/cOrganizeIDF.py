import os, shutil
'''
In the above folder, there are 38 folders, each folder contains a `in.idf` file.
saved_folder = "./resources-22-2-0"
copy all the `in.idf` files to the saved_folder, rename them as `in_uwyo_1.idf`, `in_uwyo_2.idf`, etc.
'''

source_folder = r"C:\Users\wulic\uouwyo38\run\baseline_scenario"
source_folder = r"C:\Users\wulic\la3urbanopt\run\baseline_scenario"
source_folder = "/home/xxx/la38uo/run/baseline_scenario"
source_folder = r"C:\Users\wulic\uwyo-simplified\run\baseline_scenario"
saved_folder = "./resources-22-2-0"
saved_folder = "./wy-simpified-22-2-0"
saved_file_prefix = "in_uwyo_simplified_"
#make the saved_folder if it does not exist
if not os.path.exists(saved_folder):
    os.makedirs(saved_folder)
# get all the file names in the source_folder
subfolders = os.listdir(source_folder)

# copy all the `in.idf` files to the saved_folder, rename them as `in_uwyo_1.idf`, `in_uwyo_2.idf`, etc.
for curfolder in subfolders:
    #if curfolder is not a folder, skip
    if not os.path.isdir(os.path.join(source_folder, curfolder)):
        continue
    source_file = os.path.join(source_folder, curfolder, "in.idf")
    if not os.path.exists(source_file):
        continue

    #  change1= C:/Users/wulic/uouwyo38/run/baseline_scenario/1/generated_files/future_hourly_co2e_2030.csv, !- File Name
    #  change2 = C:/Users/wulic/uouwyo38/run/baseline_scenario/1/generated_files/historical_hourly_co2e_2019.csv, !- File Name
    change1str = f"generated_files/future_hourly_co2e_2030.csv, !- File Name"
    change2str = f"generated_files/historical_hourly_co2e_2019.csv, !- File Name"
    changto1str = f"    future_hourly_co2e_2030.csv, !- File Name"
    changto2str = f"    historical_hourly_co2e_2019.csv, !- File Name"
    #find the lines containing change1str, change it to "future_hourly_co2e_2030.csv, !- File Name"
    #find the lines containing change2str, change it to "historical_hourly_co2e_2019.csv, !- File Name"
    lines_to_add = '''\
    ConvergenceLimits,
      0,                       !- Minimum System Timestep {minutes}
      25;                      !- Maximum HVAC Iterations
    '''

    #find lines containing change1str and change2str, delete that line, and add changto1str and changto2str
    with open(source_file, 'r') as file:
        for line in file:
            if change1str in line:
                lines_to_add += changto1str + "\n"
                continue
            if change2str in line:
                lines_to_add += changto2str + "\n"
                continue
            lines_to_add += line

    saved_file = os.path.join(saved_folder, saved_file_prefix + curfolder + ".idf")
    #save the modified file in saved_file
    with open(saved_file, 'w') as file:
        file.write(lines_to_add)