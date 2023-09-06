import os, shutil
'''
In the above folder, there are 38 folders, each folder contains a `in.idf` file.
saved_folder = "./resources-22-2-0"
copy all the `in.idf` files to the saved_folder, rename them as `in_uwyo_1.idf`, `in_uwyo_2.idf`, etc.
'''


source_folder = r"C:\Users\wulic\Documents\GitHub\fortran_experiments\_10Cheyenne\iLA38IDFs\la-resources-22-23-72hrs"
saved_folder = r"C:\Users\wulic\Documents\GitHub\fortran_experiments\_10Cheyenne\iLA38IDFs\la-resources-22-23-72hrs"
#make the saved_folder if it does not exist
if not os.path.exists(saved_folder):
    os.makedirs(saved_folder)
# get all the file names in the source_folder

source_text = """
  RunPeriod,
    Run Period 1,            !- Name
    9,                       !- Begin Month
    25,                      !- Begin Day of Month
    2009,                    !- Begin Year
    9,                       !- End Month
    25,                      !- End Day of Month
    2009,                    !- End Year
    Friday,                  !- Day of Week for Start Day
    No,                      !- Use Weather File Holidays and Special Days
    No,                      !- Use Weather File Daylight Saving Period
    No,                      !- Apply Weekend Holiday Rule
    Yes,                     !- Use Weather File Rain Indicators
    Yes;                     !- Use Weather File Snow Indicators
"""

target_text = """
  RunPeriod,
    Run Period 1,            !- Name
    9,                       !- Begin Month
    24,                      !- Begin Day of Month
    2009,                    !- Begin Year
    9,                       !- End Month
    26,                      !- End Day of Month
    2009,                    !- End Year
    Thursday,                  !- Day of Week for Start Day
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

