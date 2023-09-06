import os, shutil
'''
In the above folder, there are 38 folders, each folder contains a `in.idf` file.
saved_folder = "./resources-22-2-0"
copy all the `in.idf` files to the saved_folder, rename them as `in_uwyo_1.idf`, `in_uwyo_2.idf`, etc.
'''

source_folder = r"C:\Users\wulic\uouwyo38\run\baseline_scenario"
source_folder = r"C:\Users\wulic\la3urbanopt\run\baseline_scenario"
source_folder = "/home/xxx/la38uo/run/baseline_scenario"
saved_folder = "./resources-22-2-0"
saved_folder = "./la38-22-2-0"
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
    change1str = " /home/xxx/la38uo/run/baseline_scenario/38/generated_files/historical_hourly_co2e_2019.csv, !- File Name"
    change2str = "/home/xxx/la38uo/run/baseline_scenario/38/generated_files/future_hourly_co2e_2030.csv, !- File Name"
    #find the lines containing change1str, change it to "future_hourly_co2e_2030.csv, !- File Name"
    #find the lines containing change2str, change it to "historical_hourly_co2e_2019.csv, !- File Name"
    lines_to_add = '''\
    ConvergenceLimits,
      0,                       !- Minimum System Timestep {minutes}
      25;                      !- Maximum HVAC Iterations
    '''


    with open(source_file, 'r') as file:
        filedata = file.read()
    #find lines containing change1str and change2str, change them to the new strings
    filedata = filedata.replace(change1str, "future_hourly_co2e_2030.csv, !- File Name")
    filedata = filedata.replace(change2str, "historical_hourly_co2e_2019.csv, !- File Name")
    #add lines_to_add to the beginning of the file
    filedata = lines_to_add + filedata

    saved_file = os.path.join(saved_folder, "in_uwyo_" + curfolder + ".idf")
    #save the modified file in saved_file
    with open(saved_file, 'w') as file:
        file.write(filedata)


