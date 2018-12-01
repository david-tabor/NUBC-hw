import os, csv

# Read in budget_data.csv
csv_path = os.path.join(".", "budget_data.csv")
with open(csv_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    next(csv_reader, None)
    for row in csv_reader:
        print(row)