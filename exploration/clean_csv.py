import csv

# Read the CSV file, remove line breaks, and store cleaned data
input_file = 'affiliations_countries.csv'
output_file = 'affiliations_countries_cleaned.csv'

# Open the input file for reading
with open(input_file, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    rows = []

    for row in reader:
        # Concatenate all the fields in the row, remove line breaks, and strip leading/trailing whitespace
        for i in range(len(row)):
            row[i] = row[i].replace('\n', ' ').replace('\r', ' ').strip()
        rows.append(row)

print(rows)
# Open the output file for writing
with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    # Write all the cleaned rows back to the file
    writer.writerows(rows)