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
    Online Cooling Electricity Consumption[GJ], Online Cooling Electricity Demand [W],
    Consumption Difference [GJ], Consumption Difference [%], Demand Difference [W], Demand Difference [%]
'''
import os, pandas as pd
import concurrent.futures

experiments_paths = {
    # "1km_6hr": "/glade/scratch/lichenwu/IDFs38_ep_temp",
    # "100m_jun30": r"/glade/scratch/lichenwu/jun30_100mIDFs38_ep_temp",
    # "100m_july1": r"/glade/scratch/lichenwu/july1_100mIDFs38_ep_temp",
    # "100m_july2": r"/glade/scratch/lichenwu/july2_100mIDFs38_ep_temp",
    "1km_6hr": r"C:\Users\wulic\IDFs38_ep_temp\IDFs38_ep_temp",
    "100m_jun30": r"C:\Users\wulic\june30_100mIDFs38_ep_temp\june30_100mIDFs38_ep_temp",
    "100m_july1" : r"C:\Users\wulic\july1_100mIDFs38_ep_temp\july1_100mIDFs38_ep_temp",
    "100m_july2" : r"C:\Users\wulic\july2_100mIDFs38_ep_temp\july2_100mIDFs38_ep_temp",
}

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
    consumption_gj = float(curtable[3][1][2])
    demand_w = float(curtable[20][1][3])
    print("consumption_gj: ", consumption_gj)
    print("demand_w: ", demand_w)
    return [int(bld_name), ifonline, consumption_gj, demand_w]

def one_tab(parent_folder):
    two_d_tabdata = [[0,0,0,0,0,0,0,0] for i in range(38)]
    case_counter = 0
    for subfoler in os.listdir(parent_folder):
        if not os.path.isdir(os.path.join(parent_folder, subfoler)):
            continue
        print("case_counter: ", case_counter)
        case_counter += 1
        bld_name, ifonline, consumption_gj, demand_w = subfolder_to_dict(parent_folder, subfoler)
        if ifonline:
            two_d_tabdata[bld_name-1][2] = consumption_gj
            two_d_tabdata[bld_name-1][3] = demand_w
        else:
            two_d_tabdata[bld_name-1][0] = consumption_gj
            two_d_tabdata[bld_name-1][1] = demand_w
    for i in range(38):
        two_d_tabdata[i][4] = two_d_tabdata[i][2] - two_d_tabdata[i][0]
        # if division by zero, then set to NaN
        two_d_tabdata[i][5] = 100*(two_d_tabdata[i][4] / two_d_tabdata[i][0]) if two_d_tabdata[i][0] != 0 else float('NaN')
        two_d_tabdata[i][6] = two_d_tabdata[i][3] - two_d_tabdata[i][1]
        two_d_tabdata[i][7] = 100*(two_d_tabdata[i][6] / two_d_tabdata[i][1]) if two_d_tabdata[i][1] != 0 else float('NaN')
    return two_d_tabdata


def all_tabs():
    for exp_name, exp_path in experiments_paths.items():
        df = pd.DataFrame(one_tab(exp_path))
        # most left column name is "Building Number"
        df.columns = ["Offline Cooling Electricity Consumption[GJ]", "Offline Cooling Electricity Demand [W]",
                    "Online Cooling Electricity Consumption[GJ]", "Online Cooling Electricity Demand [W]",
                    "Consumption Difference [GJ]", "Consumption Difference [%]", "Demand Difference [W]", "Demand Difference [%]"]
        # name index column as "Building Number"
        df.index.name = "Building Number"
        # change index from 0, 1, 2, ... to 1, 2, 3, ...
        df.index += 1
        df.to_csv(exp_name + ".csv")

def CSVs_to_one_excel():
    excel_writer = pd.ExcelWriter("WRF-EP-Coupling.xlsx")
    new_df = None
    for exp_name in experiments_paths.keys():
        df = pd.read_csv(exp_name + ".csv")
        df.to_excel(excel_writer, sheet_name=exp_name)
        if exp_name == "1km_6hr":
            continue
        if new_df is None:
            new_df = df
            continue
        # new df columns 1,3 are sum of all other dataframes; columns 2,4 are max of all other dataframes.
        new_df.iloc[:, 1] += df.iloc[:, 1]
        new_df.iloc[:, 3] += df.iloc[:, 3]
        new_df.iloc[:, 2] = new_df.iloc[:, 2].combine(df.iloc[:, 2], max)
        new_df.iloc[:, 4] = new_df.iloc[:, 4].combine(df.iloc[:, 4], max)

    # new_df columns 5,6 are difference of columns 1,3; columns 7,8 are difference of columns 2,4.
    # Calculate the differences and percentages directly using vectorized operations
    new_df["Consumption Difference [GJ]"] = new_df["Online Cooling Electricity Consumption[GJ]"] - new_df["Offline Cooling Electricity Consumption[GJ]"]
    new_df["Consumption Difference [%]"] = 100 * (new_df["Consumption Difference [GJ]"] / new_df["Offline Cooling Electricity Consumption[GJ]"]).where(new_df["Offline Cooling Electricity Consumption[GJ]"] != 0, float('NaN'))

    new_df["Demand Difference [W]"] = new_df["Online Cooling Electricity Demand [W]"] - new_df["Offline Cooling Electricity Demand [W]"]
    new_df["Demand Difference [%]"] = 100 * (new_df["Demand Difference [W]"] / new_df["Offline Cooling Electricity Demand [W]"]).where(new_df["Offline Cooling Electricity Demand [W]"] != 0, float('NaN'))
    new_df.to_excel(excel_writer, sheet_name="Accumulated")
    with excel_writer:
        pass

if __name__ == "__main__":
    all_tabs()
    CSVs_to_one_excel()