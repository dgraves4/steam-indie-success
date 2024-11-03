import requests
import json
import os
from dotenv import load_dotenv
import csv
import time
import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Load the environment variables from .env file (API key)
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

# Check if the API key is loaded successfully
if not STEAM_API_KEY:
    print('API key not found. Please ensure the .env file is correctly set up.')
    exit()
else:
    print('API key loaded successfully.')

# Setting up requests session with retry logic to handle transient errors
session = requests.Session()
retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
session.mount('http://', HTTPAdapter(max_retries=retries))

# Get a list of all Steam app unique game IDs
def get_app_list():
    """
    Retrieves the list of all games on Steam through the Steam API.
    """
    url = "http://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = session.get(url)

    if response.status_code == 200:
        app_data = response.json()
        app_list = app_data.get('applist', {}).get('apps', [])
        return app_list
    else:
        print("Failed to get the app list.")
        return []

# Gather detailed data for the selected list of games
def get_detailed_data(app_ids, rate_limit=10):
    """
    Gathers detailed information for each app ID provided.
    Saves the collected data in a CSV file named 'steam_indie_games_balanced.csv'.
    """
    data = []
    count = 0

    for app_id in app_ids:
        url = f"http://store.steampowered.com/api/appdetails?appids={app_id}&key={STEAM_API_KEY}"
        response = session.get(url)

        if response.status_code == 200:
            try:
                app_data = response.json()

                if str(app_id) in app_data and app_data[str(app_id)]['success']:
                    details = app_data[str(app_id)]['data']

                    genres = [genre['description'] for genre in details.get('genres', [])]
                    if 'Indie' in genres:
                        game_name = details.get('name', 'N/A')
                        release_date = details.get('release_date', {}).get('date', 'N/A')
                        developer = ", ".join(details.get('developers', [])) if 'developers' in details else 'N/A'
                        genres_str = ", ".join(genres)
                        price = details.get('price_overview', {}).get('final', 0) / 100 if 'price_overview' in details else 'Free'
                        recommendations = details.get('recommendations', {}).get('total', 0)

                        data.append({
                            'AppID': app_id,
                            'Game Name': game_name,
                            'Release Date': release_date,
                            'Developer': developer,
                            'Genres': genres_str,
                            'Price ($)': price,
                            'Recommendations': recommendations
                        })

                        count += 1
                        print(f"Collected data for AppID: {app_id} ({game_name})")

            except json.JSONDecodeError:
                print(f"Error parsing JSON for app_id {app_id}")

        # Rate limit: wait to avoid overwhelming the server
        if count % rate_limit == 0:
            time.sleep(60)

    # Balance the dataset based on recommendations in three categories: low, moderate, and high
    low_recommendation_games = [game for game in data if game['Recommendations'] <= 50]
    moderate_recommendation_games = [game for game in data if 50 < game['Recommendations'] <= 500]
    high_recommendation_games = [game for game in data if game['Recommendations'] > 500]

    # Limit each group to a balanced size for data robustness
    balanced_data = (
        random.sample(low_recommendation_games, min(100, len(low_recommendation_games))) + 
        random.sample(moderate_recommendation_games, min(100, len(moderate_recommendation_games))) + 
        random.sample(high_recommendation_games, min(100, len(high_recommendation_games)))
    )

    # Save the collected balanced data into a CSV file named 'steam_indie_games_balanced.csv'
    with open('steam_indie_games_balanced.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['AppID', 'Game Name', 'Release Date', 'Developer', 'Genres', 'Price ($)', 'Recommendations'])
        writer.writeheader()
        writer.writerows(balanced_data)

    print('Data successfully saved to steam_indie_games_balanced.csv')

# Collect data for selected list of games (app IDs)
all_games = get_app_list()

# Sampling a subset of games to reduce the request load and maintain diversity
selected_app_ids = random.sample([game['appid'] for game in all_games], min(500, len(all_games)))

# Fetch the detailed data for each selected game
get_detailed_data(selected_app_ids)


