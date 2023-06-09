import os
import pathlib
import pandas as pd
import sqlite3


def read_sql(sql_path):
    if not os.path.exists(sql_path):
        return 0, 0
    abs_sql_path = os.path.abspath(sql_path)
    sql_uri = '{}?mode=ro'.format(pathlib.Path(abs_sql_path).as_uri())

    with sqlite3.connect(sql_uri, uri=True) as con:
        cursor = con.cursor()

    queryEnergyConsumption_GJ = f"SELECT * FROM TabularDataWithStrings WHERE " \
                             f"ReportName = 'AnnualBuildingUtilityPerformanceSummary' " \
                             f"AND TableName = 'End Uses'" \
            f" AND RowName = 'Cooling' AND ColumnName = 'Electricity'"
    queryEnergyDemand_W = f"SELECT * FROM TabularDataWithStrings WHERE ReportName = 'DemandEndUseComponentsSummary' " \
                          f"AND TableName = 'End Uses'" \
            f" AND RowName = 'Cooling' AND ColumnName = 'Electricity'"
    cursor.execute(queryEnergyConsumption_GJ)
    result_GJ = cursor.fetchall()
    cursor.execute(queryEnergyDemand_W)
    result_W = cursor.fetchall()
    return float(result_GJ[0][1]), float(result_W[0][1])

if __name__ == '__main__':
    parent_folder = r'C:\Users\wulic\uouwyo38\run\baseline_scenario'
    parent_folder = r"/glade/scratch/lichenwu/ep_temp/"
    buildingPerformance = {}
    for i in range(1, 39):
        curPath = parent_folder + "\\" + str(i) + "\\" + "eplusout.sql"
        curPath = parent_folder + "/" + f"ep_trivial_{i}/eplusout.sql"
        curGJ,curW = read_sql(curPath)
        print(f'{i}th building: {curGJ} GJ, {curW} W')
        buildingPerformance[i] = [curGJ, curW]

    #save the buildingPerformance to a Excel file

    df = pd.DataFrame.from_dict(buildingPerformance, orient='index', columns=['Cooling Energy Consumption GJ', 'Cooling Energy Demand W'])
    # df.to_excel('onlyURBANopt.xlsx')
    df.to_excel('WRFAndURBANopt.xlsx')