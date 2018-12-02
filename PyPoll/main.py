import os, csv

# Read in election_data.csv
data = []
csv_path = os.path.join(".", "election_data.csv")
with open(csv_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    next(csv_reader, None) #skip header
    for row in csv_reader:
        data.append({"voter_id": row[0], "county": row[1], "candidate": row[2]})


# Generate a list of the unique values of "candidate" in data
candidates = list(set( [row["candidate"] for row in data] )) 
print(candidates)

election_results = []
for candidate in candidates:
    election_results.append({"candidate": candidate, "votes": 0})

print(election_results)

# Generate summary statistics

#count = len(data)
#print(count)

#election_results = []
#for row in data:
