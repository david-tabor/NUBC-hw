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
election_results = []
for candidate in candidates:
    election_results.append({"candidate": candidate, "votes": 0})

# Count number of votes for each candidate and store in election_results
for row in data:
    for election_result in election_results:
        if election_result["candidate"] == row["candidate"]:
            election_result["votes"] += 1

# Generate summary statistics
total_vote_count = 0
winner = ""
winner_vote_count = 0
for election_result in election_results:
    total_vote_count += election_result["votes"]
    if election_result["votes"] > winner_vote_count:
        winner = election_result["candidate"]
        winner_vote_count = election_result["votes"]

# Print results
print(f'Election Results')
print(f'-------------------------')
print(f'Total Votes: {total_vote_count}')
print(f'-------------------------')
for election_result in election_results:
    print(f'{election_result["candidate"]}: ' 
    + f'{round(election_result["votes"]/total_vote_count*100.0,3)}% '
    + f'({election_result["votes"]})')
print(f'-------------------------')
print(f'Winner: {winner}')
print(f'-------------------------')

# Write data summary to file
file = open("output.txt", "w")
file.write(f'Election Results\n')
file.write(f'-------------------------\n')
file.write(f'Total Votes: {total_vote_count}\n')
file.write(f'-------------------------\n')
for election_result in election_results:
    file.write(f'{election_result["candidate"]}: ' 
    + f'{round(election_result["votes"]/total_vote_count*100.0,3)}% '
    + f'({election_result["votes"]})\n')
file.write(f'-------------------------\n')
file.write(f'Winner: {winner}\n')
file.write(f'-------------------------\n')
file.close()
