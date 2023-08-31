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

target_text = """
  RunPeriod,
    Run Period 1,            !- Name
    7,                       !- Begin Month
    2,                       !- Begin Day of Month
    2022,                    !- Begin Year
    7,                       !- End Month
    2,                       !- End Day of Month
    2022,                    !- End Year
    Saturday,                  !- Day of Week for Start Day
    No,                      !- Use Weather File Holidays and Special Days
    No,                      !- Use Weather File Daylight Saving Period
    No,                      !- Apply Weekend Holiday Rule
    Yes,                     !- Use Weather File Rain Indicators
    Yes;                     !- Use Weather File Snow Indicators
"""

source_text = """
  RunPeriod,
    Run Period 1,            !- Name
    7,                       !- Begin Month
    1,                      !- Begin Day of Month
    2022,                    !- Begin Year
    7,                       !- End Month
    1,                       !- End Day of Month
    2022,                    !- End Year
    Friday,                !- Day of Week for Start Day
    No,                      !- Use Weather File Holidays and Special Days
    No,                      !- Use Weather File Daylight Saving Period
    No,                      !- Apply Weekend Holiday Rule
    Yes,                     !- Use Weather File Rain Indicators
    Yes;                     !- Use Weather File Snow Indicators
"""

# iterate source_folder, find all *.idf files
for curidf in os.listdir(source_folder):
    #if curfolder is not a idf file, skip
    if not curidf.endswith(".idf"):
        continue
    #get the full path of the idf file
    source_file = source_folder + "\\" + curidf

    with open(source_file, 'r') as file:
        filedata = file.read()
    #find lines containing change1str and change2str, change them to the new strings
    filedata = filedata.replace(source_text, target_text)
    #save the file to original file
    with open(source_file, 'w') as file:
        file.write(filedata)

