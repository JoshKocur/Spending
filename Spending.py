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
    return filedialog.askdirectory(parent=root,initialdir="/Users",title='Please select a directory')


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
    :precond -- csv file MUST have categories named "Category" and "Expense Category Total" and they MUST have the same
    number of rows
    :param csv_file:
    :return: spending_dict a python dictionary
    """
    with open(csv_file) as csvFile:
        reader = csv.DictReader(csvFile)
        dollar_amounts = []
        category_names = []
        for row in reader:
            if is_number(row["Expense Category Total"]):  # Accounts for empty entry
                dollar_amounts.append(row["Expense Category Total"])
            if len(row["Category"]) > 0:  # Accounts for empty entries
                category_names.append(row["Category"])
    spending_dict = {}
    for x in range(0, len(dollar_amounts)):
        spending_dict.update({category_names[x]: dollar_amounts[x]})
    return spending_dict


def get_yearly_ammounts(file_path):
    yearly_savings = 0
    yearly_spending = 0
    yearly_income = 0
    for csv in get_all_csv_dir(file_path):
        yearly_savings+=float(get_monthly_reports(csv)['Savings'])
        yearly_income+=float(get_monthly_reports(csv)['Income'])
        yearly_spending+=float(get_monthly_reports(csv)['Spending'])
    return {'Yearly Savings': yearly_savings, 'Yearly Income': yearly_income,
            'Yearly Spending': yearly_spending}


def get_avg_monthly_values(file_path):
    yearly_values = get_yearly_ammounts(file_path)
    avg_values = []
    for key in yearly_values:
        yearly_values[key] /= len(get_all_csv_dir(file_path))
        avg_values.append(yearly_values[key])
    avg_dict = {"Avg Monthly Savings": avg_values[0], "Avg Monthly Income": avg_values[1],
                "Avg Monthly Spending": avg_values[2]}
    return avg_dict


if __name__ == "__main__":
    try:
        csv_dir = sys.argv[1]
    except IndexError:
        csv_dir = get_csv_dir()

    print("Yearly Ammounts %s"%(get_yearly_ammounts(csv_dir)))
    print("A typical Month %s"%(get_avg_monthly_values(csv_dir)))
    for csv_file in get_all_csv_dir(csv_dir):
        print(os.path.basename(csv_file))
        print("    %s"%(get_monthly_reports(csv_file)))
        print("    %s"%(get_spending_category_data(csv_file)))