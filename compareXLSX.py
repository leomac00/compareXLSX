import pandas as pd
import numpy as np
import copy
import sys


def print_sheets_comparison(names_list1, names_list2, names_intersection):
    differences = (set(names_list1).difference(set(names_intersection))).union(
        (set(names_list2).difference(set(names_intersection))))
    print(' - Mismatching sheets found: ', differences)


def print_values_comparison(sheet1, sheet2):
    print('---------- X ----------')
    try:
        comparison_values = sheet1.values == sheet2.values
        rows, cols = np.where(comparison_values is False and comparison_values is not np.nan)
        copied_sheet = copy.deepcopy(sheet1)
        for item in zip(rows, cols):
            copied_sheet.iloc[item[0], item[1]] = '[{}]~[{}]'.format(sheet1.iloc[item[0], item[1]],
                                                                     sheet2.iloc[item[0], item[1]])
        print(copied_sheet)
    except Exception as e :
        print("The files could not be compared, this happened:\n-->" + e)
    finally:
        print('---------- X ----------')


if __name__ == '__main__':
    #	Get files to be compared
    xlsx_file_names = ['./' + sys.argv[1], './' + sys.argv[2]]

    # Comparing sheets inside workbook and getting the intersected items to be compared next
    sheet_names1 = pd.ExcelFile(xlsx_file_names[0]).sheet_names
    sheet_names2 = pd.ExcelFile(xlsx_file_names[1]).sheet_names
    sheet_names_intersection = list(set(sheet_names1) & set(sheet_names2))
    are_sheets_equal = sheet_names1 == sheet_names2
    print('\n--->  Comparing sheets inside both workbooks...')
    print('Same sheets between both items? -> ' + str(are_sheets_equal))
    if not are_sheets_equal:
        print_sheets_comparison(sheet_names1, sheet_names2, sheet_names_intersection)

    # Comparing values inside each sheet
    print('\n--->   Comparing values inside each sheet...')
    for i in range(len(sheet_names_intersection)):
        df1 = pd.read_excel(xlsx_file_names[0], sheet_names_intersection[i])
        df2 = pd.read_excel(xlsx_file_names[1], sheet_names_intersection[i])
        are_values_equal = df1.equals(df2)
        print('Both sheets \'' + sheet_names_intersection[i] + '\' match? -> ' + str(are_values_equal))
        if not df1.equals(df2):
            print_values_comparison(df1, df2)
