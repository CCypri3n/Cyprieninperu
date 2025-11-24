import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('GOATCOUNTER_API_TOKEN')

if not API_TOKEN:
    raise ValueError("API token not found. Please set GOATCOUNTER_API_TOKEN in your .env file.")

file_path = 'content/extra/viewcounts.json'

SITE = 'https://cyprieninperu.goatcounter.com/api/v0'
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json',
}

def fetch_view_counts():
    url = f"{SITE}/stats/hits"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    # Create mapping: path -> count
    counts = {item['path']: item['count'] for item in data['hits']}
    print(counts)
    return counts

if __name__ == "__main__":
    counts = fetch_view_counts()
    with open(file_path, 'w') as f:
        import json
        json.dump(counts, f)
