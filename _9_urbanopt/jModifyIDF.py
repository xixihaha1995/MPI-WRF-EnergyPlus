import os, shutil
'''
In the above folder, there are 38 folders, each folder contains a `in.idf` file.
saved_folder = "./resources-22-2-0"
copy all the `in.idf` files to the saved_folder, rename them as `in_uwyo_1.idf`, `in_uwyo_2.idf`, etc.
'''


source_folder = r"C:\Users\wulic\Documents\GitHub\fortran_experiments\_10Cheyenne\h38IDFs\resources-23-1-0"
saved_folder = r"C:\Users\wulic\Documents\GitHub\fortran_experiments\_10Cheyenne\h38IDFs\resources-23-1-0"
#make the saved_folder if it does not exist
if not os.path.exists(saved_folder):
    os.makedirs(saved_folder)
# get all the file names in the source_folder
subfolders = os.listdir(source_folder)

source_text = """
  RunPeriod,
    Run Period 1,            !- Name
    5,                       !- Begin Month
    1,                       !- Begin Day of Month
    2023,                    !- Begin Year
    5,                       !- End Month
    1,                       !- End Day of Month
    2023,                    !- End Year
    Monday,                  !- Day of Week for Start Day
    No,                      !- Use Weather File Holidays and Special Days
    No,                      !- Use Weather File Daylight Saving Period
    No,                      !- Apply Weekend Holiday Rule
    Yes,                     !- Use Weather File Rain Indicators
    Yes;                     !- Use Weather File Snow Indicators
"""

target_text = """
  RunPeriod,
    Run Period 1,            !- Name
    6,                       !- Begin Month
    30,                      !- Begin Day of Month
    2022,                    !- Begin Year
    7,                       !- End Month
    2,                       !- End Day of Month
    2022,                    !- End Year
    Thursday,                !- Day of Week for Start Day
    No,                      !- Use Weather File Holidays and Special Days
    No,                      !- Use Weather File Daylight Saving Period
    No,                      !- Apply Weekend Holiday Rule
    Yes,                     !- Use Weather File Rain Indicators
    Yes;                     !- Use Weather File Snow Indicators
"""

# copy all the `in.idf` files to the saved_folder, rename them as `in_uwyo_1.idf`, `in_uwyo_2.idf`, etc.
for curfolder in subfolders:
    #if curfolder is not a folder, skip
    if not os.path.isdir(source_folder + "\\" + curfolder):
        continue
    source_file = source_folder + "\\" + curfolder + "\\" + "in.idf"
    if not os.path.exists(source_file):
        continue

    #  change1= C:/Users/wulic/uouwyo38/run/baseline_scenario/1/generated_files/future_hourly_co2e_2030.csv, !- File Name
    #  change2 = C:/Users/wulic/uouwyo38/run/baseline_scenario/1/generated_files/historical_hourly_co2e_2019.csv, !- File Name

    #find the lines containing change1str, change it to "future_hourly_co2e_2030.csv, !- File Name"
    #find the lines containing change2str, change it to "historical_hourly_co2e_2019.csv, !- File Name"


    with open(source_file, 'r') as file:
        filedata = file.read()
    #find lines containing change1str and change2str, change them to the new strings
    filedata = filedata.replacereplace(source_text, target_text)
    #add lines_to_add to the beginning of the file

    saved_file = saved_folder + "\\" + "in_" + str(curfolder) + ".idf"
    #save the modified file in saved_file
    with open(saved_file, 'w') as file:
        file.write(filedata)


