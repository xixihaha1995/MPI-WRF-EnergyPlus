'''
I have four experiments: 1km_6hr, 100m_jun30, 100m_jul1, 100m_jul2
In each experiment, there are 38 * 2 = 76 folders, which contains either online or offline building performance results in eplustbl.htm files.
folder names have the following formates:
saved_offline_ep_trivial_1
saved_online2_waste_surf_ep_trivial_38

I'd like to organize the results in excel file, each tab is an experiment,
row: 1 to 38
columns: 
    Offline Cooling Electricity Consumption[GJ], Offline Cooling Electricity Demand [W],
    Offline Heating Natural Gas[GJ], Offline Heating Natural Gas[W],
    Online Cooling Electricity Consumption[GJ], Online Cooling Electricity Demand [W],
    Online Heating Natural Gas[GJ], Online Heating Natural Gas[W],
or
    TMY3 Cooling Electricity Consumption[GJ], TMY3 Cooling Electricity Demand [W],
    TMY3 Heating Natural Gas[GJ], TMY3 Heating Natural Gas[W]
'''
import os, pandas as pd

import numpy as np
import openpyxl

experiments_paths = {
    # "1km_6hr": "/glade/scratch/lichenwu/IDFs38_ep_temp",
    # "100m_jun30": r"/glade/scratch/lichenwu/jun30_100mIDFs38_ep_temp",
    # "100m_july1": r"/glade/scratch/lichenwu/july1_100mIDFs38_ep_temp",
    # "100m_july2": r"/glade/scratch/lichenwu/july2_100mIDFs38_ep_temp",
    "WY_1km_6hr": r"C:\Users\wulic\IDFs38_ep_temp\IDFs38_ep_temp",
    "WY_TMY3": r"C:\Users\wulic\TMY3_WY_IDFs38_ep_temp\TMY3_WY_IDFs38_ep_temp",
    "WY_100m_jun30": r"C:\Users\wulic\june30_100mIDFs38_ep_temp\june30_100mIDFs38_ep_temp",
    "WY_100m_july1" : r"C:\Users\wulic\july1_100mIDFs38_ep_temp\july1_100mIDFs38_ep_temp",
    "WY_100m_july2" : r"C:\Users\wulic\july2_100mIDFs38_ep_temp\july2_100mIDFs38_ep_temp",
}

def calculate_percentage_difference(row, rowNumerator, rowDenominator):
    if rowDenominator != 0:
        return 100 * (rowNumerator / rowDenominator)
    else:
        return np.nan
def read_html(html_path):
    if not os.path.exists(html_path):
        return 0, 0
    abs_html_path = os.path.abspath(html_path)
    with open(abs_html_path, 'r') as f:
        html = f.read()
    rt = pd.read_html(html)
    return rt

def subfolder_to_dict(parent_folder, subfolder):
    bld_name = subfolder.split("_")[-1]
    print("parent_folder: ", parent_folder, " subfolder: ", subfolder)
    ifonline = "online" in subfolder
    # detect if current os is windows or linux
    curtable = read_html(os.path.join(parent_folder, subfolder, "eplustbl.htm"))
    clConGJ = float(curtable[3][1][2])
    clDemW = float(curtable[20][1][3])
    htConGJ = float(curtable[3][2][1])
    htDemW = float(curtable[20][2][2])
    return [int(bld_name), ifonline, clConGJ,clDemW, htConGJ,htDemW]

def one_tab(parent_folder):
    if "TMY3" in parent_folder:
        two_d_tabdata = [[0 for i in range(4)] for j in range(38)]
    else:
        two_d_tabdata = [[0 for i in range(8)] for j in range(38)]
    case_counter = 0
    for subfoler in os.listdir(parent_folder):
        if not os.path.isdir(os.path.join(parent_folder, subfoler)):
            continue
        print("case_counter: ", case_counter)
        case_counter += 1
        bld_name, ifonline, clConGJ,clDemW, htConGJ,htDemW = subfolder_to_dict(parent_folder, subfoler)
        print("bld_name: ", bld_name, " ifonline: ", ifonline, " clConGJ: ", clConGJ, " clDemW: ", clDemW, " htConGJ: ", htConGJ, " htDemW: ", htDemW)
        if ifonline:
            two_d_tabdata[bld_name-1][4] = clConGJ
            two_d_tabdata[bld_name-1][5] = clDemW
            two_d_tabdata[bld_name-1][6] = htConGJ
            two_d_tabdata[bld_name-1][7] = htDemW
        else:
            two_d_tabdata[bld_name-1][0] = clConGJ
            two_d_tabdata[bld_name-1][1] = clDemW
            two_d_tabdata[bld_name-1][2] = htConGJ
            two_d_tabdata[bld_name-1][3] = htDemW

    return two_d_tabdata

def all_tabs():
    for exp_name, exp_path in experiments_paths.items():
        df = pd.DataFrame(one_tab(exp_path))
        # most left column name is "Building Number"
        if 'TMY3' in exp_name:
            df.columns = ["TMY3 Cooling Electricity Consumption[GJ]", "TMY3 Cooling Electricity Demand [W]",
                            "TMY3 Heating Natural Gas[GJ]", "TMY3 Heating Natural Gas[W]"]
        else:
            df.columns = ["Offline Cooling Electricity Consumption[GJ]", "Offline Cooling Electricity Demand [W]",
                            "Offline Heating Natural Gas[GJ]", "Offline Heating Natural Gas[W]",
                            "Online Cooling Electricity Consumption[GJ]", "Online Cooling Electricity Demand [W]",
                            "Online Heating Natural Gas[GJ]", "Online Heating Natural Gas[W]"]


        # name index column as "Building Number"
        df.index.name = "Building Number"
        # change index from 0, 1, 2, ... to 1, 2, 3, ...
        df.index += 1
        df.to_csv(exp_name + ".csv")

def CSVs_to_one_excel():
    excel_writer = pd.ExcelWriter(excel_name)
    new_df = None
    for exp_name in experiments_paths.keys():
        df = pd.read_csv(exp_name + ".csv")
        df.to_excel(excel_writer, sheet_name=exp_name)
        if "1km" in exp_name or "TMY3" in exp_name:
            continue
        if new_df is None:
            new_df = df
            continue
        # new_df.columns
        # Index(['Building Number', 'Offline Cooling Electricity Consumption[GJ]',
        #        'Offline Cooling Electricity Demand [W]',
        #        'Offline Heating Natural Gas[GJ]', 'Offline Heating Natural Gas[W]',
        #        'Online Cooling Electricity Consumption[GJ]',
        #        'Online Cooling Electricity Demand [W]',
        #        'Online Heating Natural Gas[GJ]', 'Online Heating Natural Gas[W]'],
        #       dtype='object')
        # odd columns should be summed, even columns should be maxed
        len_columns = len(new_df.columns)
        for i in range(1, len_columns, 2):
            new_df.iloc[:, i] += df.iloc[:, i]
        for i in range(2, len_columns, 2):
            new_df.iloc[:, i] = new_df.iloc[:, i].combine(df.iloc[:, i], max)

    # new_df columns 5,6 are difference of columns 1,3; columns 7,8 are difference of columns 2,4.
    # Calculate the differences and percentages directly using vectorized operations
    # new_df["Consumption Difference [GJ]"] = new_df["Online Cooling Electricity Consumption[GJ]"] - new_df["Offline Cooling Electricity Consumption[GJ]"]
    # new_df["Consumption Difference [%]"] = 100 * (new_df["Consumption Difference [GJ]"] / new_df["Offline Cooling Electricity Consumption[GJ]"]).where(new_df["Offline Cooling Electricity Consumption[GJ]"] != 0, float('NaN'))
    #
    # new_df["Demand Difference [W]"] = new_df["Online Cooling Electricity Demand [W]"] - new_df["Offline Cooling Electricity Demand [W]"]
    # new_df["Demand Difference [%]"] = 100 * (new_df["Demand Difference [W]"] / new_df["Offline Cooling Electricity Demand [W]"]).where(new_df["Offline Cooling Electricity Demand [W]"] != 0, float('NaN'))
    added_columns = ["DiffClConGJ", "DiffClDemW", "DiffHtConGJ", "DiffHtDemW", "DiffClCon%", "DiffClDem%", "DiffHtCon%", "DiffHtDem%"]
    for i in range(0,4):
        new_df[added_columns[i]] = new_df.iloc[:, i + 5] - new_df.iloc[:, i + 1]
    for i in range(0,4):
        new_df[added_columns[i + 4]] = 100 * (new_df.iloc[:, i + 5] - new_df.iloc[:, i + 1]) / new_df.iloc[:, i + 1]

    new_df.to_excel(excel_writer, sheet_name="Accumulated")
    with excel_writer:
        pass



def comparied_to_tmy3():
    pass
    '''
    There are 4 metric, clConGJ, clDemW, htConGJ, htDemW
    There are 3 cases, tmy3, offline, online
    We will compare offline and online to tmy3: 
        DiffClConGJ, DiffClDemW, DiffHtConGJ, DiffHtDemW
        DiffClCon%, DiffClDem%, DiffHtCon%, DiffHtDem%
    '''
    # open excel, new_sheet should be initialized from WY_TMY3
    _sheetName = "CompareToTMY3"
    _excel = openpyxl.load_workbook(excel_name)
    _tmy3DF = pd.read_excel(excel_name, sheet_name="WY_TMY3")
    _accuDF = pd.read_excel(excel_name, sheet_name="Accumulated")
    '''
    new sheet columns:
        tmy3 columns, offline columns, online columns, 
        off diff columns, on diff columns,
        off diff % columns, on diff % columns
    '''

    newShtNames =     ["BldgNum", "TMY3CoolElec(GJ)", "TMY3CoolElecDemand(W)", "TMY3HeatNatGas(GJ)", "TMY3HeatNatGas(W)",
     "OfflineCoolElec(GJ)", "OfflineCoolElecDemand(W)", "OfflineHeatNatGas(GJ)", "OfflineHeatNatGas(W)",
     "OnlineCoolElec(GJ)", "OnlineCoolElecDemand(W)", "OnlineHeatNatGas(GJ)", "OnlineHeatNatGas(W)",
     "OfflineCoolElecDiff(GJ)", "OfflineCoolElecDemandDiff(W)", "OfflineHeatNatGasDiff(GJ)", "OfflineHeatNatGasDiff(W)",
     "OnlineCoolElecDiff(GJ)", "OnlineCoolElecDemandDiff(W)", "OnlineHeatNatGasDiff(GJ)", "OnlineHeatNatGasDiff(W)",
     "OfflineCoolConDiff%", "OfflineCoolDemDiff%", "OfflineHeatConDiff%", "OfflineHeatDemDiff%",
        "OnlineCoolConDiff%", "OnlineCoolDemDiff%", "OnlineHeatConDiff%", "OnlineHeatDemDiff%"]
    _newDF = pd.DataFrame(columns=newShtNames)
    '''
    1. first copy all tmy3 data to new sheet
    2. then copy all accumulated data (except the first BldgNum column) to new sheet
    '''
    tmy3DFColLen = len(_tmy3DF.columns)
    accuDFColLen = len(_accuDF.columns) - 8
    _newDF.iloc[:,0:tmy3DFColLen-1] = _tmy3DF.iloc[:,1:tmy3DFColLen]
    _newDF.iloc[:,tmy3DFColLen-1:tmy3DFColLen+accuDFColLen-3] = _accuDF.iloc[:,2:accuDFColLen]

    _newDF["OfflineCoolElecDiff(GJ)"] = _newDF["OfflineCoolElec(GJ)"] - _newDF["TMY3CoolElec(GJ)"]
    _newDF["OfflineCoolElecDemandDiff(W)"] = _newDF["OfflineCoolElecDemand(W)"] - _newDF["TMY3CoolElecDemand(W)"]
    _newDF["OfflineHeatNatGasDiff(GJ)"] = _newDF["OfflineHeatNatGas(GJ)"] - _newDF["TMY3HeatNatGas(GJ)"]
    _newDF["OfflineHeatNatGasDiff(W)"] = _newDF["OfflineHeatNatGas(W)"] - _newDF["TMY3HeatNatGas(W)"]
    _newDF["OnlineCoolElecDiff(GJ)"] = _newDF["OnlineCoolElec(GJ)"] - _newDF["TMY3CoolElec(GJ)"]
    _newDF["OnlineCoolElecDemandDiff(W)"] = _newDF["OnlineCoolElecDemand(W)"] - _newDF["TMY3CoolElecDemand(W)"]
    _newDF["OnlineHeatNatGasDiff(GJ)"] = _newDF["OnlineHeatNatGas(GJ)"] - _newDF["TMY3HeatNatGas(GJ)"]
    _newDF["OnlineHeatNatGasDiff(W)"] = _newDF["OnlineHeatNatGas(W)"] - _newDF["TMY3HeatNatGas(W)"]
    _newDF["OfflineCoolConDiff%"] = _newDF.apply(lambda row: calculate_percentage_difference(row, row["OfflineCoolElecDiff(GJ)"], row["TMY3CoolElec(GJ)"]), axis=1)
    _newDF["OfflineCoolDemDiff%"] = _newDF.apply(lambda row: calculate_percentage_difference(row, row["OfflineCoolElecDemandDiff(W)"], row["TMY3CoolElecDemand(W)"]), axis=1)
    _newDF["OfflineHeatConDiff%"] = _newDF.apply(lambda row: calculate_percentage_difference(row, row["OfflineHeatNatGasDiff(GJ)"], row["TMY3HeatNatGas(GJ)"]), axis=1)
    _newDF["OfflineHeatDemDiff%"] = _newDF.apply(lambda row: calculate_percentage_difference(row, row["OfflineHeatNatGasDiff(W)"], row["TMY3HeatNatGas(W)"]), axis=1)
    _newDF["OnlineCoolConDiff%"] = _newDF.apply(lambda row: calculate_percentage_difference(row, row["OnlineCoolElecDiff(GJ)"], row["TMY3CoolElec(GJ)"]), axis=1)
    _newDF["OnlineCoolDemDiff%"] = _newDF.apply(lambda row: calculate_percentage_difference(row, row["OnlineCoolElecDemandDiff(W)"], row["TMY3CoolElecDemand(W)"]), axis=1)
    _newDF["OnlineHeatConDiff%"] = _newDF.apply(lambda row: calculate_percentage_difference(row, row["OnlineHeatNatGasDiff(GJ)"], row["TMY3HeatNatGas(GJ)"]), axis=1)
    _newDF["OnlineHeatDemDiff%"] = _newDF.apply(lambda row: calculate_percentage_difference(row, row["OnlineHeatNatGasDiff(W)"], row["TMY3HeatNatGas(W)"]), axis=1)

    # save to excel
    with pd.ExcelWriter(excel_name, engine='openpyxl', mode='a',if_sheet_exists='replace') as excel_writer:
        _newDF.to_excel(excel_writer, sheet_name=_sheetName,index=False)


excel_name = "WRF-EP-Coupling.xlsx"
# all_tabs()
CSVs_to_one_excel()
comparied_to_tmy3()