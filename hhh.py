import pandas as pd
from datetime import datetime, timedelta

# This function will take the excel file as input and read it
def read_excel(file_path):
    return pd.read_excel(file_path)

# I have used dataframe from pandas to analyze the data
def analyze_data(df):
    # I have converting string of date and time into datatime object to manipulate it in a better way
    df['Time'] = pd.to_datetime(df['Time'])
    df['Time Out'] = pd.to_datetime(df['Time Out'])


    for employee in df['Employee Name'].unique():
        employee_data = df[df['Employee Name'] == employee]

        # Condition a: Check for 7 consecutive working days
        check_consecutive_days(employee, employee_data)

        # Condition b: Check for less than 10 hours between shifts
        check_shift_time_gap(employee, employee_data)

        # Condition c: Check for more than 14 hours in a single shift
        check_long_shifts(employee, employee_data)

# this function will check for the employee working 7 consecutive working days
def check_consecutive_days(employee, data):
    data = data.sort_values(by='Time')
    consecutive_days = 1
    previous_date = None

    for _, row in data.iterrows():
        if previous_date and (row['Time'].date() - previous_date).days == 1:
            consecutive_days += 1
            if consecutive_days == 7:
                print(f"{employee} has worked 7 consecutive days.")
                break
        else:
            consecutive_days = 1
        previous_date = row['Time'].date()

# this function will check for the employee working less than 10 hours between shifts
def check_shift_time_gap(employee, data):
    data = data.sort_values(by='Time')
    previous_shift_end = None

    for _, row in data.iterrows():
        if previous_shift_end:
            time_diff = row['Time'] - previous_shift_end
            if timedelta(hours=1) < time_diff < timedelta(hours=10):
                print(f"{employee} has less than 10 hours between shifts.")
                break
        previous_shift_end = row['Time Out']

# this function will check for the employee working for more than 14 hours in a single shift
def check_long_shifts(employee, data):
    for _, row in data.iterrows():
        if (row['Time Out'] - row['Time']).seconds > 50400:
            print(f"{employee} has worked more than 14 hours in a single shift.")
            break

# Main function
def main():
    file_path = 'Assignment_Timecard.xlsx'
    df = read_excel(file_path)
    analyze_data(df)

if __name__ == "__main__":
    main()
