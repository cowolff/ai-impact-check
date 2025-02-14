import json
import csv
from typing import List, Dict, Set
import os

# 1. Function to load the affiliation-country mapping from the CSV
def load_affiliation_country_map(csv_file: str) -> Dict[str, str]:
    affiliation_country_map = {}
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            affiliation_country_map[row['Affiliation']] = row['Country']
    return affiliation_country_map

# 2. Reuse the function to load all JSON files
def load_json_files(file_paths: List[str]) -> List[Dict[str, any]]:
    all_entries = []
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            data = json.load(f)
            all_entries.extend(data)
    return all_entries

# 3. Function to map authors' affiliations to countries
def map_authors_to_countries(entries: List[Dict[str, any]], affiliation_country_map: Dict[str, str]) -> List[Dict[str, Set[str]]]:
    papers_countries = []
    for entry in entries:
        countries = set()
        for author in entry['authors']:
            affiliation = author['affiliation']
            if affiliation in affiliation_country_map:
                countries.add(affiliation_country_map[affiliation])
        papers_countries.append({'title': entry['title'], 'countries': countries})
    return papers_countries

# 4. Function to count papers per country
def count_papers_per_country(papers_countries: List[Dict[str, Set[str]]]) -> Dict[str, int]:
    country_paper_count = {}
    for paper in papers_countries:
        for country in paper['countries']:
            country = country.strip()
            if country in country_paper_count:
                country_paper_count[country] += 1
            else:
                country_paper_count[country] = 1
    return country_paper_count

# 5. Function to print or save the country-paper counts
def print_country_paper_counts(country_paper_count: Dict[str, int]):
    for country, count in country_paper_count.items():
        print(f"{country}: {count} papers")

# Example usage
def main():
    # Step 1: Load the affiliation-country mapping from the CSV file
    csv_file = "affiliations_countries.csv"  # Replace with the actual path to your CSV file
    affiliation_country_map = load_affiliation_country_map(csv_file)

    # Step 2: Load all JSON files
    file_paths = os.listdir("data")
    file_paths = [os.path.join("data", file) for file in file_paths if file.endswith(".json")]
    all_entries = load_json_files(file_paths)

    # Step 3: Map authors' affiliations to countries
    papers_countries = map_authors_to_countries(all_entries, affiliation_country_map)

    # Step 4: Count papers per country
    country_paper_count = count_papers_per_country(papers_countries)

    # Step 5: Order by country count
    country_paper_count = dict(sorted(country_paper_count.items(), key=lambda x: x[1], reverse=True))

    # Step 6: Merge usa and United States results
    if 'USA' in country_paper_count.keys() and 'United States' in country_paper_count.keys():
        country_paper_count['United States'] += country_paper_count['USA']
        del country_paper_count['USA']

    # Step 5: Print or save the results
    print_country_paper_counts(country_paper_count)

if __name__ == "__main__":
    main()
