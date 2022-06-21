import os
import pandas as pd

xlsx_file_names = []


def print_sheet_comparison(sheet1, sheet2):
    print('---')
    print(sheet1 == sheet2)
    print('---------- X ----------\n')


for file in os.listdir('./'):
    if file.endswith('.xlsx'):
        xlsx_file_names.append(file)


if __name__ == '__main__':
    sheet_names = pd.ExcelFile(xlsx_file_names[0]).sheet_names
    for i in range(len(sheet_names)):
        df1 = pd.read_excel(xlsx_file_names[0], sheet_names[i])
        df2 = pd.read_excel(xlsx_file_names[1], sheet_names[i])
        print('Result of \'' + sheet_names[i] + '\': ' + str(df1.equals(df2)))
        if not df1.equals(df2):
            print_sheet_comparison(df1, df2)
