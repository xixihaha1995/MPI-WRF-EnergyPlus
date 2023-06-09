'''
City order:
Dubai
HoChiMinh
Honolulu
NewDelhi
Tampa
Tucson
Atlanta
ElPaso
SanDiego
NewYork
Albuquerque
Seattle
Buffalo
Denver
PortAngeles
Rochester
GreatFalls
InternationalFalls
Fairbanks
I have one excel file "C:\\Users\\wulic\\Documents\\DataProcess\\DataProcess\\EUIComparison.xlsx"
Please reorder the rows in the excel file according to the above city order.
'''
import pandas as pd
import os

if __name__ == '__main__':
    old_excel_path = r"C:\Users\wulic\Documents\DataProcess\DataProcess\EUIComparison.csv"
    new_excel_path = r"C:\Users\wulic\Documents\DataProcess\DataProcess\EUIComparisonNew.csv"
    df = pd.read_csv(old_excel_path, index_col=0)
    df = df.reindex(['Dubai','HoChiMinh','Honolulu','NewDelhi',
                        'Tampa','Tucson','Atlanta','ElPaso',
                        'SanDiego','NewYork','Albuquerque','Seattle',
                        'Buffalo','Denver','PortAngeles','Rochester',
                        'GreatFalls','InternationalFalls','Fairbanks'])

    #save to new file
    df.to_csv(new_excel_path)