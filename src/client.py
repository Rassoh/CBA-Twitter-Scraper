import os, time, requests
from dotenv import load_dotenv
from urllib.parse import quote, urlencode 

load_dotenv()
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
HEADERS = {"Authorization": f"Bearer {BEARER_TOKEN}"}

BASE = "https://api.twitter.com/2/"

def get(url, params):
    q = urlencode(params, doseq=True)
    r = requests.get(f"{BASE}{url}?{q}", headers=HEADERS, timeout = 30)
    r.raise_for_status()
    return r.json()

def paginate(url, params, limit = 1000):
    fetched = 0 
    next_token = None
    while fetched < limit:
        if next_token:
            params["next_token"] = next_token
        data = get(url, params)
        yield data
        fetched += len(data.get("data", []))
        next_token = data.get("meta", {}).get("next_token")
        if not next_token:
            break
        time.sleep(1.1)
        

