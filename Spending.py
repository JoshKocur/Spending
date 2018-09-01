import csv
import os
from tkinter import filedialog
from tkinter import *

SAVING_X_VAL = 1
SAVING_Y_VAL = 4
INCOME_X_VAL = 1
INCOME_Y_VAL = 2
SPENDING_X_VAL = 1
SPENDING_Y_VAL = 3


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_csv_dir():
    root = Tk()
    root.withdraw()
    return filedialog.askdirectory(parent=root,initialdir="/Users/Documents/Spending/2018csv",title='Please select a directory')


def get_all_csv_dir(file_path):
    csv_files = []
    for file in os.listdir(file_path):
        if file[-4:] == ".csv":
            csv_files.append(file_path+"/"+file)
    return csv_files



def get_monthly_reports(csv_file):
    with open(csv_file) as csvDataFile:
        data = [row for row in csv.reader(csvDataFile)]
    return {'Savings':data[SAVING_X_VAL][SAVING_Y_VAL], 'Income':data[INCOME_X_VAL][INCOME_Y_VAL],
            'Spending':data[SPENDING_X_VAL][SPENDING_Y_VAL]}



def get_spending_category_data(csv_file):
    """
    Returns a dictionary of spending categories and their value
    :precond -- csv file MUST have categories named "Category" and "Expense Category Total" and they must have the same
    number of rows
    :param csv_file:
    :return: spending_dict a python dictionary
    """
    with open(csv_file) as csvFile:
        reader = csv.DictReader(csvFile)
        dollar_amounts = []
        category_names = []
        for row in reader:
            if is_number(row["Expense Category Total"]):  # Accounts for empty entrie
                dollar_amounts.append(row["Expense Category Total"])
            if len(row["Category"]) > 0:  # Accounts for empty entries
                category_names.append(row["Category"])
    spending_dict = {}
    for x in range(0, len(dollar_amounts)):
        spending_dict.update({category_names[x]: dollar_amounts[x]})
    return spending_dict







list_csv = get_all_csv_dir(get_csv_dir())
for file in list_csv:
    print(os.path.basename(file))
    print(get_monthly_reports(file))
    print(get_spending_category_data(file))
