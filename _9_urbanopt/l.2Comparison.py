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

experiments_paths = {
    # "1km_6hr": "/glade/scratch/lichenwu/IDFs38_ep_temp",
    # "100m_jun30": r"/glade/scratch/lichenwu/jun30_100mIDFs38_ep_temp",
    # "100m_july1": r"/glade/scratch/lichenwu/july1_100mIDFs38_ep_temp",
    # "100m_july2": r"/glade/scratch/lichenwu/july2_100mIDFs38_ep_temp",
    # "WY_1km_6hr": r"C:\Users\wulic\IDFs38_ep_temp\IDFs38_ep_temp",
    # "WY_TMY3": r"C:\Users\wulic\TMY3_WY_IDFs38_ep_temp\TMY3_WY_IDFs38_ep_temp",
    # "WY_100m_jun30": r"C:\Users\wulic\june30_100mIDFs38_ep_temp\june30_100mIDFs38_ep_temp",
    # "WY_100m_july1" : r"C:\Users\wulic\july1_100mIDFs38_ep_temp\july1_100mIDFs38_ep_temp",
    # "WY_100m_july2" : r"C:\Users\wulic\july2_100mIDFs38_ep_temp\july2_100mIDFs38_ep_temp",
    # "LA_TMY3":r"C:\Users\wulic\TMY3_LA_IDFs38_ep_temp\TMY3_LA_IDFs38_ep_temp",
    # "LA_500m":r"C:\Users\wulic\la_72hrs500m_IDFs38_ep_temp\la_72hrs500m_IDFs38_ep_temp",
    "WY-Simple-1000m-30flrs":r"C:\Users\wulic\1000m-30flrs\1000m-30flrs",
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
    _coupling = -1
    if "offline" in subfolder:
        _coupling = 0
    elif "waste" in subfolder:
        _coupling = 1
    elif "LWR" in subfolder:
        _coupling = 2
    # detect if current os is windows or linux
    curtable = read_html(os.path.join(parent_folder, subfolder, "eplustbl.htm"))
    clConGJ = float(curtable[3][1][2])
    clDemW = float(curtable[20][1][3])
    htConGJ = float(curtable[3][2][1])
    htDemW = float(curtable[20][2][2])
    return [int(bld_name), _coupling, clConGJ,clDemW, htConGJ,htDemW]

def one_tab(parent_folder):
    if "TMY3" in parent_folder:
        two_d_tabdata = [[0 for i in range(4)] for j in range(38)]
    else:
        two_d_tabdata = [[0 for i in range(12)] for j in range(38)]
    case_counter = 0
    for subfoler in os.listdir(parent_folder):
        if not os.path.isdir(os.path.join(parent_folder, subfoler)):
            continue
        print("case_counter: ", case_counter)
        case_counter += 1
        bld_name, _coupling, clConGJ,clDemW, htConGJ,htDemW = subfolder_to_dict(parent_folder, subfoler)
        print("bld_name: ", bld_name, " _coupling: ", _coupling, " clConGJ: ", clConGJ, " clDemW: ", clDemW, " htConGJ: ", htConGJ, " htDemW: ", htDemW)

        two_d_tabdata[bld_name - 1][_coupling * 4] = clConGJ
        two_d_tabdata[bld_name - 1][_coupling * 4 + 1] = clDemW
        two_d_tabdata[bld_name - 1][_coupling * 4 + 2] = htConGJ
        two_d_tabdata[bld_name - 1][_coupling * 4 + 3] = htDemW

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
                            "Online-NoLWR Cooling Electricity Consumption[GJ]", "Online-NoLWR Cooling Electricity Demand [W]",
                            "Online-NoLWR Heating Natural Gas[GJ]", "Online-NoLWR Heating Natural Gas[W]",
                            "Online-LWR Cooling Electricity Consumption[GJ]", "Online-LWR Cooling Electricity Demand [W]",
                            "Online-LWR Heating Natural Gas[GJ]", "Online-LWR Heating Natural Gas[W]"]


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

        if new_df is None:
            new_df = df
            continue

    # new_df columns 5,6 are difference of columns 1,3; columns 7,8 are difference of columns 2,4.
    # Calculate the differences and percentages directly using vectorized operations
    # new_df["Consumption Difference [GJ]"] = new_df["Online Cooling Electricity Consumption[GJ]"] - new_df["Offline Cooling Electricity Consumption[GJ]"]
    # new_df["Consumption Difference [%]"] = 100 * (new_df["Consumption Difference [GJ]"] / new_df["Offline Cooling Electricity Consumption[GJ]"]).where(new_df["Offline Cooling Electricity Consumption[GJ]"] != 0, float('NaN'))
    #
    # new_df["Demand Difference [W]"] = new_df["Online Cooling Electricity Demand [W]"] - new_df["Offline Cooling Electricity Demand [W]"]
    # new_df["Demand Difference [%]"] = 100 * (new_df["Demand Difference [W]"] / new_df["Offline Cooling Electricity Demand [W]"]).where(new_df["Offline Cooling Electricity Demand [W]"] != 0, float('NaN'))
    added_columns = ["ColConGJ_NoLWR-Off", "ColDemW_NoLWR-Off", "HtConGJ_NoLWR-Off", "HtDemW_NoLWR-Off",
                        "ColConGJ_LWR-Off", "ColDemW_LWR-Off", "HtConGJ_LWR-Off", "HtDemW_LWR-Off",
                        "ColConGJ_LWR-NoLWR", "ColDemW_LWR-NoLWR", "HtConGJ_LWR-NoLWR", "HtDemW_LWR-NoLWR",
                        "ColCon%_NoLWR-Off", "ColDem%_NoLWR-Off", "HtCon%_NoLWR-Off", "HtDem%_NoLWR-Off",
                        "ColCon%_LWR-Off", "ColDem%_LWR-Off", "HtCon%_LWR-Off", "HtDem%_LWR-Off",
                        "ColCon%_LWR-NoLWR", "ColDem%_LWR-NoLWR", "HtCon%_LWR-NoLWR", "HtDem%_LWR-NoLWR"]
    for i in range(0,4):
        new_df[added_columns[i]] = new_df.iloc[:, i + 5] - new_df.iloc[:, i + 1]
        new_df[added_columns[i+4]] = new_df.iloc[:, i + 9] - new_df.iloc[:, i + 1]
        new_df[added_columns[i+8]] = new_df.iloc[:, i + 9] - new_df.iloc[:, i + 5]
        #  new_df[added_columns[i + 4]] = 100 * (new_df.iloc[:, i + 5] - new_df.iloc[:, i + 1]) / new_df.iloc[:, i + 1]
        new_df[added_columns[i + 12]] = 100 * (new_df.iloc[:, i + 5] - new_df.iloc[:, i + 1]) / new_df.iloc[:, i + 1]
        new_df[added_columns[i + 16]] = 100 * (new_df.iloc[:, i + 9] - new_df.iloc[:, i + 1]) / new_df.iloc[:, i + 1]
        new_df[added_columns[i + 20]] = 100 * (new_df.iloc[:, i + 9] - new_df.iloc[:, i + 5]) / new_df.iloc[:, i + 5]


    new_df.to_excel(excel_writer, sheet_name="Diff")
    with excel_writer:
        pass



excel_name = "WY-Simple-1000m-30flrs-lwr.xlsx"
all_tabs()
CSVs_to_one_excel()