from dotenv import load_dotenv
import os
import requests
import pandas as pd
import json

# Load the environment variables from .env file
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

if not STEAM_API_KEY:
    print('API key not found. Please ensure the .env file is correctly set up.')
    exit()
else:
    print('API key loaded successfully.')

# Example function to get app details from Steam API
def get_app_details(app_id):
    url = f"http://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(url)
    
    if response.status_code == 200:
        app_data = response.json()
        # For now, just print the data to check what we get
        print(json.dumps(app_data, indent=2))
    else:
        print(f"Failed to fetch data for app_id {app_id}: {response.status_code}")

# Test with an example app_id
get_app_details(440)  # Example AppID for Team Fortress 2
