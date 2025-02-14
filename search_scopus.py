import requests
import json
from dotenv import load_dotenv
import os
from tqdm import tqdm

load_dotenv()
API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://api.elsevier.com/content/search/scopus'

def get_papers_and_authors(query, num_results=10):
    """
    Fetches a list of papers, authors, and affiliations based on the search query.

    Args:
        query (str): The search string for the Scopus database.
        num_results (int): The number of results to return.

    Returns:
        list: A list of dictionaries, each containing details of a paper, authors, and affiliations.
    """
    headers = {
        'X-ELS-APIKey': API_KEY,
        'Accept': 'application/json'
    }

    steps = 10
    index = 0

    papers_info = []

    for i in tqdm(range(0, num_results, steps)):
    
        params = {
            'query': query,
            'count': steps,
            'start': i
        }
        
        response = requests.get(BASE_URL, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.json())
            return []
        
        data = response.json()

        datapoints = data.get('search-results', {}).get('entry', [])

        for entry in datapoints:
            paper_info = {
                'title': entry.get('dc:title', 'N/A'),
                'affiliations': [],
            }

            affiliations = entry.get('affiliation', {})
            
            for affiliation in affiliations:
                affiliation_info = {
                    'name': affiliation.get('affilname', 'N/A'),
                    'city': affiliation.get('affiliation-city', 'N/A'),
                    'country': affiliation.get('affiliation-country', 'N/A')
                }
                paper_info['affiliations'].append(affiliation_info)

            papers_info.append(paper_info)

        index += 10

        if len(datapoints) == 0:
            break

    return papers_info

# Example usage:
query = 'machine learning in healthcare'  # Modify this search query as needed
results = get_papers_and_authors(query, num_results=10)
print(results)