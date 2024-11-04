import requests
import json
import os
from dotenv import load_dotenv
import csv
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Load the environment variables from .env file (API key)
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

# Check if the API key is loaded successfully and if not, print an error message and exit the script
if not STEAM_API_KEY:
    print('API key not found. Please ensure the .env file is correctly set up.')
    exit()
else:
    print('API key loaded successfully.')

# Setting up requests session with retry logic to handle errors and timeouts on the server side
session = requests.Session()
retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))  # Changed to HTTPS for secure connection

# Get a list of all Steam app unique game IDs
def get_app_list():
    """
    Retrieves the list of all games on Steam through the Steam API.
    """
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    try:
        response = session.get(url)

        if response.status_code == 200:
            app_data = response.json()
            app_list = app_data.get('applist', {}).get('apps', [])
            return app_list
        else:
            print(f"Failed to get the app list. Status code: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching app list: {e}")
        return []

# Gather detailed data for the selected list of games and add a rate limit to avoid locking out the API
def get_detailed_data(app_ids, rate_limit=20, min_games=300):
    """
    Gathers detailed information for each app ID provided.
    Saves the collected data in CSV files.
    """
    data = []
    count = 0
    sleep_duration = 10

    while len(data) < min_games:
        for app_id in app_ids:
            if len(data) >= min_games:
                break

            url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
            try:
                response = session.get(url)

                if response.status_code == 200:
                    try:
                        app_data = response.json()

                        if str(app_id) in app_data and app_data[str(app_id)]['success']:
                            details = app_data[str(app_id)]['data']

                            genres = [genre['description'] for genre in details.get('genres', [])]
                            if 'Indie' in genres and 'Adult' not in genres and not details.get('type', '').lower() == 'dlc' and not details.get('type', '').lower() == 'demo':
                                game_name = details.get('name', 'N/A')
                                release_date = details.get('release_date', {}).get('date', 'N/A')
                                developer = ", ".join(details.get('developers', [])) if 'developers' in details else 'N/A'
                                genres_str = ", ".join(genres)
                                price = details.get('price_overview', {}).get('final', 0) / 100 if 'price_overview' in details else 'Free'
                                recommendations = details.get('recommendations', {}).get('total', 0)
                                metacritic_score = details.get('metacritic', {}).get('score', 'N/A')

                                # Skip games that are still in development
                                if 'Coming soon' in release_date or 'Early Access' in genres_str:
                                    continue

                                data.append({
                                    'AppID': app_id,
                                    'Game Name': game_name,
                                    'Release Date': release_date,
                                    'Developer': developer,
                                    'Genres': genres_str,
                                    'Price ($)': price,
                                    'Recommendations': recommendations,
                                    'Metacritic Score': metacritic_score
                                })

                                count += 1
                                print(f"Collected data for AppID: {app_id} ({game_name})")

                    except json.JSONDecodeError:
                        print(f"Error parsing JSON for app_id {app_id}")

                elif response.status_code == 429:
                    print(f"Rate limit hit for AppID {app_id}. Status code: 429. Sleeping for {sleep_duration} seconds.")
                    time.sleep(sleep_duration)
                    sleep_duration = min(sleep_duration * 2, 120)  # Exponential backoff
                    continue

                elif response.status_code == 403:
                    print(f"Access forbidden for AppID {app_id}. Status code: 403. Skipping.")

                else:
                    print(f"Failed to get details for AppID {app_id}. Status code: {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"Error occurred while fetching app details for AppID {app_id}: {e}")

            if count % rate_limit == 0 and count > 0:
                print(f"Rate limiting: Sleeping for {sleep_duration} seconds...")
                time.sleep(sleep_duration)

        if len(data) < min_games:
            print(f"Insufficient data collected ({len(data)}/{min_games}). Resampling app IDs...")
            app_ids = random.sample([game['appid'] for game in all_games], min(5000, len(all_games)))

    # Filter games with at least a minimum number of recommendations
    MIN_RECOMMENDATIONS = 5
    filtered_data = [game for game in data if game['Recommendations'] >= MIN_RECOMMENDATIONS]

    # Balance the dataset based on recommendations categories proportionally
    low_recommendation_games = [game for game in filtered_data if game['Recommendations'] <= 50]
    moderate_recommendation_games = [game for game in filtered_data if 50 < game['Recommendations'] <= 500]
    high_recommendation_games = [game for game in filtered_data if game['Recommendations'] > 500]

    # Ensure the sample size does not exceed the available population
    low_recommendation_games = random.sample(low_recommendation_games, min(100, len(low_recommendation_games)))
    moderate_recommendation_games = random.sample(moderate_recommendation_games, min(100, len(moderate_recommendation_games)))
    high_recommendation_games = random.sample(high_recommendation_games, min(100, len(high_recommendation_games)))

    # Combine all categories to get the balanced dataset
    balanced_data = low_recommendation_games + moderate_recommendation_games + high_recommendation_games

    # Save the collected balanced data into a CSV file named 'steam_indie_games_balanced.csv'
    with open('steam_indie_games_balanced.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['AppID', 'Game Name', 'Release Date', 'Developer', 'Genres', 'Price ($)', 'Recommendations', 'Metacritic Score'])
        writer.writeheader()
        writer.writerows(balanced_data)

    # Save all the collected data before balancing
    with open('steam_indie_games_all.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['AppID', 'Game Name', 'Release Date', 'Developer', 'Genres', 'Price ($)', 'Recommendations', 'Metacritic Score'])
        writer.writeheader()
        writer.writerows(data)

    print('Data successfully saved to steam_indie_games_balanced.csv and steam_indie_games_all.csv')

# Collect data for selected list of games (app IDs)
all_games = get_app_list()

# Sampling a larger subset of games to increase the chances of getting enough valid data
selected_app_ids = random.sample([game['appid'] for game in all_games], min(5000, len(all_games)))

# Fetch the detailed data for each selected game
get_detailed_data(selected_app_ids, min_games=300)









