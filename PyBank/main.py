import os, csv

# Read in budget_data.csv
data = []
csv_path = os.path.join(".", "budget_data.csv")
with open(csv_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    next(csv_reader, None) #skip header
    for row in csv_reader:
        data.append({"Date": row[0], "Profit/Loss": float(row[1])})

# Generate summary statistics

count = len(data)
sum_profitloss = 0.0
max_change = {"Date": "", "Profit/Loss": 0.0}
min_change = {"Date": "", "Profit/Loss": 0.0}
for row in data:
    sum_profitloss += row["Profit/Loss"]
    if row["Profit/Loss"] > max_change["Profit/Loss"]:
        max_change["Date"] = row["Date"]
        max_change["Profit/Loss"] = row["Profit/Loss"]
    if row["Profit/Loss"] < min_change["Profit/Loss"]:
        min_change["Date"] = row["Date"]
        min_change["Profit/Loss"] = row["Profit/Loss"]
average_profitloss = sum_profitloss / count
 
# Print data summary
print("Financial Analysis:")
print("----------------------------")
print(f'Total Months: {count}')
print(f'Total: $ {sum_profitloss}')
print(f'Average Change: $ {average_profitloss}')
print(f'Greatest Increase in Profits: {max_change["Date"]} ($ {max_change["Profit/Loss"]})')
print(f'Greatest Decrease in Profits: {min_change["Date"]} ($ {min_change["Profit/Loss"]})')
