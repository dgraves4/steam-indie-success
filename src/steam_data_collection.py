import requests
import json
import os
from dotenv import load_dotenv
import csv
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load the environment variables from the .env file, specifically the API key needed for accessing the Steam API.
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

# Check if the API key is loaded successfully. If not, print an error message and exit the script.
if not STEAM_API_KEY:
    print('API key not found. Please ensure the .env file is correctly set up.')
    exit()
else:
    print('API key loaded successfully.')

# Setting up a requests session with retry logic to handle any HTTP errors (500, 502, 503, 504) to avoid data loss.
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504, 429])
session.mount('https://', HTTPAdapter(max_retries=retries))  # Using HTTPS for secure communication

# Function to retrieve a list of all game IDs available on Steam.
def get_app_list():
    """
    Retrieves the list of all games on Steam through the Steam API.
    """
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    try:
        response = session.get(url, timeout=10)

        # If the request is successful, extract and return the list of game apps.
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

# Function to gather detailed information for a selected list of games.
def get_detailed_data(app_ids, min_games=300):
    """
    Gathers detailed information for each app ID provided.
    Saves the collected data in a CSV file.
    """
    data = []  # List to store detailed information of games

    def fetch_app_details(app_id):
        url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
        retries = 3  # Number of retries for each request
        for attempt in range(retries):
            try:
                response = session.get(url, timeout=10)
                if response.status_code == 200:
                    app_data = response.json()
                    if str(app_id) in app_data and app_data[str(app_id)]['success']:
                        details = app_data[str(app_id)]['data']
                        genres = [genre['description'] for genre in details.get('genres', [])]
                        if 'Indie' in genres and details.get('type', '').lower() not in ['dlc', 'demo']:
                            game_name = details.get('name', 'N/A')
                            release_date = details.get('release_date', {}).get('date', 'N/A')
                            developer = ", ".join(details.get('developers', [])) if 'developers' in details else 'N/A'
                            genres_str = ", ".join(genres)
                            price = details.get('price_overview', {}).get('final', 0) / 100 if 'price_overview' in details else 'Free'
                            recommendations = details.get('recommendations', {}).get('total', 0)
                            metacritic_score = details.get('metacritic', {}).get('score', 'N/A')

                            return {
                                'AppID': app_id,
                                'Game Name': game_name,
                                'Release Date': release_date,
                                'Developer': developer,
                                'Genres': genres_str,
                                'Price ($)': price,
                                'Recommendations': recommendations,
                                'Metacritic Score': metacritic_score
                            }
                elif response.status_code == 429:
                    # Handle rate limiting with exponential backoff
                    sleep_time = 2 ** (attempt + 1)
                    print(f"Rate limit hit for AppID {app_id}. Sleeping for {sleep_time} seconds.")
                    time.sleep(sleep_time)
                else:
                    print(f"Attempt {attempt + 1} failed for AppID {app_id}. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} error for AppID {app_id}: {e}")
            time.sleep(5)  # Wait before retrying
        return None

    # Use ThreadPoolExecutor to speed up the data collection process.
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_app_id = {executor.submit(fetch_app_details, app_id): app_id for app_id in app_ids}
        for future in as_completed(future_to_app_id):
            app_id = future_to_app_id[future]
            try:
                result = future.result()
                if result:
                    data.append(result)
                    print(f"Collected data for AppID: {app_id} ({result['Game Name']})")
            except Exception as e:
                print(f"Error fetching details for AppID {app_id}: {e}")

    # Filter the collected data to include only games with at least a minimum number of 1 recommendation.
    MIN_RECOMMENDATIONS = 1
    filtered_data = [game for game in data if game['Recommendations'] >= MIN_RECOMMENDATIONS]

    # Balance the dataset by selecting as many games as possible from different recommendation categories.
    low_recommendation_games = [game for game in filtered_data if game['Recommendations'] <= 50]
    moderate_recommendation_games = [game for game in filtered_data if 50 < game['Recommendations'] <= 500]
    high_recommendation_games = [game for game in filtered_data if game['Recommendations'] > 500]

    # Collect games from each category, allowing for unbalanced totals if necessary.
    balanced_data = (
        random.sample(low_recommendation_games, min(100, len(low_recommendation_games))) +
        random.sample(moderate_recommendation_games, min(100, len(moderate_recommendation_games))) +
        random.sample(high_recommendation_games, min(100, len(high_recommendation_games)))
    )

    # If we still don't have enough data, use all that is available.
    if len(balanced_data) < min_games:
        balanced_data = filtered_data[:min_games]

    # Save the balanced dataset to a CSV file.
    with open('steam_indie_games_balanced.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['AppID', 'Game Name', 'Release Date', 'Developer', 'Genres', 'Price ($)', 'Recommendations', 'Metacritic Score'])
        writer.writeheader()
        writer.writerows(balanced_data)

    print(f'Data successfully saved to steam_indie_games_balanced.csv with {len(balanced_data)} records.')

# Collect the complete list of games from Steam.
all_games = get_app_list()

# Sample a subset of game IDs (10000) to increase the chances of collecting enough valid data for analysis.
selected_app_ids = random.sample([game['appid'] for game in all_games], min(10000, len(all_games)))

# Fetch detailed data for each selected game, aiming to collect data for at least 300 games.
get_detailed_data(selected_app_ids, min_games=300)



















