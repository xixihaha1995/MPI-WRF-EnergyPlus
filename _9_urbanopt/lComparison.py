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
    ifonline = "online" in subfolder
    # detect if current os is windows or linux
    iflinux = os.name == 'posix'
    curtable = read_html(os.path.join(parent_folder, subfolder, "eplustbl.htm")) \
        if iflinux else read_html(os.path.join(parent_folder, subfolder, "ASHRAE901_ApartmentMidRise_STD2007_Albuquerque.table.htm"))
    consumption_gj = curtable[3][1][2]
    demand_w = curtable[17][1][3]
    return [int(bld_name), ifonline, consumption_gj, demand_w]

def one_tab(parent_folder):
    two_d_tabdata = [[0,0,0,0,0,0,0,0] for i in range(38)]
    for subfoler in os.listdir(parent_folder):
#         if not folder then continue
        if not os.path.isdir(os.path.join(parent_folder, subfoler)):
            continue
        bld_name, ifonline, consumption_gj, demand_w = subfolder_to_dict(parent_folder, subfoler)
        if ifonline:
            two_d_tabdata[bld_name-1][2] = consumption_gj
            two_d_tabdata[bld_name-1][3] = demand_w
        else:
            two_d_tabdata[bld_name-1][0] = consumption_gj
            two_d_tabdata[bld_name-1][1] = demand_w
    for i in range(38):
        two_d_tabdata[i][4] = two_d_tabdata[i][2] - two_d_tabdata[i][0]
        two_d_tabdata[i][5] = two_d_tabdata[i][4] / two_d_tabdata[i][0]
        two_d_tabdata[i][6] = two_d_tabdata[i][3] - two_d_tabdata[i][1]
        two_d_tabdata[i][7] = two_d_tabdata[i][6] / two_d_tabdata[i][1]
    print(two_d_tabdata)
    return two_d_tabdata


def all_tabs(name):
    experiments_paths = {
        "1km_6hr": "/glade/scratch/lichenwu/IDFs38_ep_temp",
        # "100m_jun30": r"/glade/scratch/lichenwu/jun30_100mIDFs38_ep_temp",
        # "100m_jul1": r"/glade/scratch/lichenwu/july1_100mIDFs38_ep_temp",
        # "100m_jul2": r"/glade/scratch/lichenwu/july2_100mIDFs38_ep_temp"
    }

    excel_writer = pd.ExcelWriter(name)
    for exp_name, exp_path in experiments_paths.items():
        df = pd.DataFrame(one_tab(exp_path))
        df.columns = ["Offline Cooling Electricity Consumption[GJ]", "Offline Cooling Electricity Demand [W]",
                      "Online Cooling Electricity Consumption[GJ]", "Online Cooling Electricity Demand [W]",
                      "Consumption Difference [GJ]", "Consumption Difference [%]", "Demand Difference [W]", "Demand Difference [%]"]
        df.to_excel(excel_writer, sheet_name=exp_name)
    excel_writer.save()

if __name__ == "__main__":
    all_tabs("urbanopt_comparison.xlsx")
