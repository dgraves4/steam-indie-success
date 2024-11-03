import requests
import json
import os
from dotenv import load_dotenv
import csv

# Load the environment variables from .env file (API key)
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

# Check if the API key is loaded successfully
if not STEAM_API_KEY:
    print('API key not found. Please ensure the .env file is correctly set up.')
    exit()
else:
    print('API key loaded successfully.')

# Get a list of all Steam app unique game IDs
def get_app_list():
    """
    Retrieves the list of all games on Steam through the Steam API.
    """
    url = "http://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(url)

    # Check if the response from the API was successful (status code 200 means success)
    if response.status_code == 200:
        app_data = response.json()
        # Extracting the list of apps/games from the response
        app_list = app_data.get('applist', {}).get('apps', [])
        return app_list
    else:
        # Print an error message if the API request fails
        print("Failed to get the app list.")
        return []

# Gather our detailed data for the selected list of games
def get_detailed_data(app_ids):
    """
    Gathers detailed information for each app ID provided.
    Saves the collected data in a CSV file named 'steam_indie_games.csv'.
    """
    data = []  # To store the collected data
    count = 0  # Counter to keep track of the number of games processed
    
    for app_id in app_ids:
        # Limit to 300 games for size considerations
        if count >= 300:
            break

        # Construct the API URL for getting the details of each app by app with f-string
        url = f"http://store.steampowered.com/api/appdetails?appids={app_id}&key={STEAM_API_KEY}"
        response = requests.get(url)

        # If the response from the API was successful, parse the data
        if response.status_code == 200:
            try:
                app_data = response.json()
                
                # Verify if the app data is available and the request was successful
                if str(app_id) in app_data and app_data[str(app_id)]['success']:
                    details = app_data[str(app_id)]['data']
                    
                    # Extract genres and check if the game is labeled as "Indie"
                    genres = [genre['description'] for genre in details.get('genres', [])]
                    if 'Indie' in genres:
                        # Extract relevant information about each game
                        game_name = details.get('name', 'N/A')
                        release_date = details.get('release_date', {}).get('date', 'N/A')
                        developer = ", ".join(details.get('developers', [])) if 'developers' in details else 'N/A'
                        genres_str = ", ".join(genres)
                        price = details.get('price_overview', {}).get('final', 0) / 100 if 'price_overview' in details else 'Free'
                        recommendations = details.get('recommendations', {}).get('total', 'N/A')

                        # Append collected details into the data list
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
            except json.JSONDecodeError:
                # Handle any errors that occur when trying to parse the JSON response
                print(f"Error parsing JSON for app_id {app_id}")

    # Save the collected data into a CSV file named 'steam_indie_games.csv'
    with open('steam_indie_games.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['AppID', 'Game Name', 'Release Date', 'Developer', 'Genres', 'Price ($)', 'Recommendations'])
        writer.writeheader()  # Write the header row with column names
        writer.writerows(data)  # Write all the collected data rows

    print('Data successfully saved to steam_indie_games.csv')

# Collect data for selected list of games (app IDs)
# Get the list of all games using the Steam API
all_games = get_app_list()
# Extract all app IDs from the list
selected_app_ids = [game['appid'] for game in all_games]
# Fetch the detailed data for each selected game
get_detailed_data(selected_app_ids)



