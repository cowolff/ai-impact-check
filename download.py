import requests

# Define base URL for datasets API
base_url = "https://api.semanticscholar.org/datasets/v1/release/"

# To get the list of available releases make a request to the base url. No additional parameters needed.
response = requests.get(base_url)

# Print the response data
date = response.json()[-1]

base_url = "https://api.semanticscholar.org/datasets/v1/release/"

# Make a request to get datasets available the latest release
response = requests.get(base_url + date)

# Print the response data
print(response.json())