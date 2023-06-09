'''
I need process html files.
One sample file name is "ASHRAE901_ApartmentMidRise_STD2007_Albuquerque.table.htm"
Separated by "_" there are 4 parts:
1. ASHRAE901
2. ApartmentMidRise
3. STD2007
4. Albuquerque

You will construct a dictionary, the key is the 4th part,
the value is a list of 8 items:
HighRise_2007_NaturalGas_MJ_m2
HighRise_2019_NaturalGas_MJ_m2
HighRise_2007_Electricity_MJ_m2
HighRise_2019_Electricity_MJ_m2
MidRise_2007_NaturalGas_MJ_m2
MidRise_2019_NaturalGas_MJ_m2
MidRise_2007_Electricity_MJ_m2
MidRise_2019_Electricity_MJ_m2

Parent folder: r'C:\\Users\\wulic\\Documents\\DataProcess\\DataProcess'
And it has 2 subfolders: Highrise and Midrise
'''
import os
import pathlib
import pandas as pd


def read_html(html_path):
    if not os.path.exists(html_path):
        return 0, 0
    abs_html_path = os.path.abspath(html_path)
    with open(abs_html_path, 'r') as f:
        html = f.read()
    rt = pd.read_html(html)
    return rt

if __name__ == '__main__':
    parent_folder = r'C:\Users\wulic\Documents\DataProcess\DataProcess'
    colIndex = ['HighRise_2007_NaturalGas_MJ_m2',
                'HighRise_2019_NaturalGas_MJ_m2',
                'HighRise_2007_Electricity_MJ_m2',
                'HighRise_2019_Electricity_MJ_m2',
                'MidRise_2007_NaturalGas_MJ_m2',
                'MidRise_2019_NaturalGas_MJ_m2',
                'MidRise_2007_Electricity_MJ_m2',
                'MidRise_2019_Electricity_MJ_m2']
    EUIComparison = {}
    count = 0
    for subfolder in ['Highrise', 'Midrise']:
        for filename in os.listdir(parent_folder + "\\" + subfolder):
            if filename.endswith(".htm"):
                print(filename)
                count += 1
                # if count > 3:
                #     break
                _4thpart = filename.split("_")[3].split(".")[0]
                if _4thpart not in EUIComparison.keys():
                    EUIComparison[_4thpart] = [0, 0, 0, 0, 0, 0, 0, 0]
                curPath = parent_folder + "\\" + subfolder + "\\" + filename
                _curtable = read_html(curPath)
                totalBuildingAreaM2 = float(_curtable[2][1][1])
                electricityGJ = float(_curtable[3][1][16])
                naturalGasGJ = float(_curtable[3][2][16])
                # format as .2f
                electricityMJ_m2 = float("{:.2f}".format(electricityGJ / totalBuildingAreaM2 * 1000))
                naturalGasMJ_m2 = float("{:.2f}".format(naturalGasGJ / totalBuildingAreaM2 * 1000))
                if "2007" in filename:
                    if "HighRise" in filename:
                        EUIComparison[_4thpart][0] = naturalGasMJ_m2
                        EUIComparison[_4thpart][2] = electricityMJ_m2
                    else:
                        EUIComparison[_4thpart][4] = naturalGasMJ_m2
                        EUIComparison[_4thpart][6] = electricityMJ_m2
                else:
                    if "HighRise" in filename:
                        EUIComparison[_4thpart][1] = naturalGasMJ_m2
                        EUIComparison[_4thpart][3] = electricityMJ_m2
                    else:
                        EUIComparison[_4thpart][5] = naturalGasMJ_m2
                        EUIComparison[_4thpart][7] = electricityMJ_m2
    #save key as row index

    df = pd.DataFrame.from_dict(EUIComparison, orient='index', columns=colIndex)
    df = df.reindex(['Dubai','HoChiMinh','Honolulu','NewDelhi',
                        'Tampa','Tucson','Atlanta','ElPaso',
                        'SanDiego','NewYork','Albuquerque','Seattle',
                        'Buffalo','Denver','PortAngeles','Rochester',
                        'GreatFalls','InternationalFalls','Fairbanks'])
    df.to_csv(parent_folder + "\\" + "EUIComparison.csv")