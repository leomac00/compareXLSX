import pandas as pd
import numpy as np
import copy
import os



def print_values_comparison(sheet1, sheet2):
    print('---------- X ----------')
    comparison_values = sheet1.values == sheet2.values 
    rows,cols = np.where(comparison_values == False)
    copied_sheet = copy.deepcopy(sheet1)
    for item in zip(rows, cols):
        copied_sheet.iloc[item[0], item[1]] = '[{}]~[{}]'.format(sheet1.iloc[item[0], item[1]], sheet2.iloc[item[0], item[1]])
    print(copied_sheet)
    print('---------- X ----------')



if __name__ == '__main__':
    # Get files to be compared
    xlsx_file_names = []
    for file in os.listdir('./'):
        if file.endswith('.xlsx'):
            xlsx_file_names.append(file)
    
    #Comparing sheets inside workbook and getting the intersected items to be compared next
    sheet_names1 = pd.ExcelFile(xlsx_file_names[0]).sheet_names
    sheet_names2 = pd.ExcelFile(xlsx_file_names[1]).sheet_names
    sheet_names = list(set(sheet_names1) & set(sheet_names2))
    are_sheets_equal = sheet_names1 == sheet_names2
    print('\n--->  Comparing sheets inside both workbooks...')
    print('Same sheets between both items? -> ' + str(are_sheets_equal))
    if not are_sheets_equal:
        differences = (set(sheet_names1).difference(set(sheet_names))).union((set(sheet_names2).difference(set(sheet_names))))
        print(' - Mismatching sheets found: ', differences)
        
    #Comparing values inside each sheet
    print('\n--->   Comparing values inside each sheet...')
    for i in range(len(sheet_names)):
        df1 = pd.read_excel(xlsx_file_names[0], sheet_names[i])
        df2 = pd.read_excel(xlsx_file_names[1], sheet_names[i])
        print('Both sheets \'' + sheet_names[i] + '\' match? -> ' + str(df1.equals(df2)))
        if not df1.equals(df2):
            print_values_comparison(df1, df2)
