# This is the backbone of the application. this class is used to send api requests to the poe.ninja
# site and retrieve the answer.

import requests
import poe_types

currentLeague = 'Standard'

item_types = poe_types.item_types
reward_Types = poe_types.reward_types
unique_types = poe_types.unique_types

def send_request(overview, league, type):
    api_url = f"https://poe.ninja/api/data/{overview}?league={league}&type={type}"

    try:
        # Send GET request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Save the raw response content in a variable
            api_response = response.content.decode('utf-8')
            return api_response
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.RequestException as e:
        print(f"Request failed: {e}")

# GUI
# WEITERE KATEGORIEN
# FILTER IM GUI
# UNIQUE Karten Fixen bei calculate divs
# DISCORD Functions statt messages
