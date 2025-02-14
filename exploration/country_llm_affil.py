import json
import os
import csv
from typing import List, Dict, Any, Set
from mlx_lm import load, generate
import tqdm

# 1. Function to load all JSON files and concatenate lists
def load_json_files(file_paths: List[str]) -> List[Dict[str, Any]]:
    all_entries = []
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            data = json.load(f)
            all_entries.extend(data)
    return all_entries

# 2. Function to extract unique affiliations
def extract_unique_affiliations(entries: List[Dict[str, Any]]) -> Set[str]:
    unique_affiliations = set()
    for entry in entries:
        for author in entry['authors']:
            unique_affiliations.add(author['affiliation'])
    return unique_affiliations

# 3. Function to query an LLM for the country of an affiliation
def get_country_for_affiliation(affiliation: str, llm_function) -> str:
    # Here, `llm_function` is a placeholder for whatever function/API you use to query the LLM.
    # Example: return llm_function(f"What country is the affiliation '{affiliation}' from?")
    return llm_function(affiliation)  # This should be replaced with the actual call to the LLM

# 4. Function to map affiliations to countries
def map_affiliations_to_countries(affiliations: Set[str], llm_function) -> Dict[str, str]:
    affiliation_country_map = {}
    with tqdm.tqdm(total=len(affiliations)) as pbar:
        for affiliation in affiliations:
            country = get_country_for_affiliation(affiliation, llm_function)
            affiliation_country_map[affiliation] = country
            pbar.update(1)
    return affiliation_country_map

# 5. Function to save the results to a CSV file
def save_to_csv(affiliation_country_map: Dict[str, str], output_csv: str):
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Affiliation', 'Country'])
        for affiliation, country in affiliation_country_map.items():
            writer.writerow([affiliation, country])

# Example usage
def main():
    # Step 1: Load all JSON files
    list_of_all_entries = os.listdir("data")
    file_paths = [os.path.join("data", file) for file in list_of_all_entries if file.endswith(".json")]
   
    all_entries = load_json_files(file_paths)

    # Step 2: Extract unique affiliations
    unique_affiliations = extract_unique_affiliations(all_entries)

    model, tokenizer = load("mlx-community/Meta-Llama-3.1-8B-Instruct-8bit")

    # Step 3 & 4: Map affiliations to countries using a hypothetical LLM function
    # Replace `dummy_llm_function` with your actual LLM function
    def dummy_llm_function(affiliation: str) -> str:
        prompt = "What country is the affiliation '" + affiliation + "' from. Only answer with one word in the form of the country. Give back NA if you don't know?"
        prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
        generated = generate(model, tokenizer, prompt, max_tokens=4)
        return generated # Replace this with real country detection logic

    affiliation_country_map = map_affiliations_to_countries(unique_affiliations, dummy_llm_function)

    # Step 5: Save the results to a CSV file
    save_to_csv(affiliation_country_map, "affiliations_countries.csv")

if __name__ == "__main__":
    main()