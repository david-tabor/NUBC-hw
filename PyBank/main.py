import csv

csvreader = csv.reader(open("budget_data.csv"))
next(csvreader)

for row in csvreader:
    print(row)