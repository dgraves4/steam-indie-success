import requests
import json
import os
from dotenv import load_dotenv
import csv

# Load the environment variables from .env file
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

if not STEAM_API_KEY:
    print('API key not found. Please ensure the .env file is correctly set up.')
    exit()
else:
    print('API key loaded successfully.')

# Get a list of app IDs
def get_app_list():
    url = "http://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(url)

    if response.status_code == 200:
        app_data = response.json()
        app_list = app_data.get('applist', {}).get('apps', [])
        # Filtering for indie games only (keyword: indie on steam)
        indie_games = [app for app in app_list if "indie" in app['name'].lower() or "indie" in app['name'].lower()]
        return indie_games
    else:
        print("Failed to get the app list.")
        return []

# Step 3.2: Gather Detailed Data for Each Selected Game
def get_detailed_data(app_ids):
    data = []
    count = 0
    for app_id in app_ids:
        if count >= 300:  # Limit to 300 games
            break

        url = f"http://store.steampowered.com/api/appdetails?appids={app_id}&key={STEAM_API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            try:
                app_data = response.json()
                if str(app_id) in app_data and app_data[str(app_id)]['success']:
                    details = app_data[str(app_id)]['data']
                    # Collect relevant information
                    game_name = details.get('name', 'N/A')
                    release_date = details.get('release_date', {}).get('date', 'N/A')
                    developer = ", ".join(details.get('developers', [])) if 'developers' in details else 'N/A'
                    genres = ", ".join([genre['description'] for genre in details.get('genres', [])]) if 'genres' in details else 'N/A'
                    price = details.get('price_overview', {}).get('final', 0) / 100 if 'price_overview' in details else 'Free'
                    recommendations = details.get('recommendations', {}).get('total', 'N/A')

                    data.append({
                        'AppID': app_id,
                        'Game Name': game_name,
                        'Release Date': release_date,
                        'Developer': developer,
                        'Genres': genres,
                        'Price ($)': price,
                        'Recommendations': recommendations
                    })
                    count += 1
            except json.JSONDecodeError:
                print(f"Error parsing JSON for app_id {app_id}")

    # Save to CSV file
    with open('steam_indie_games.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['AppID', 'Game Name', 'Release Date', 'Developer', 'Genres', 'Price ($)', 'Recommendations'])
        writer.writeheader()
        writer.writerows(data)

    print('Data successfully saved to steam_indie_games.csv')

# Collect data for selected list of games (app IDs)
indie_games = get_app_list()
selected_app_ids = [game['appid'] for game in indie_games[:300]]  # Select the first 300 indie games for simplicity
get_detailed_data(selected_app_ids)

