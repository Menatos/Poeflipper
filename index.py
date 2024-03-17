# This is the backbone of the application. this class is used to send api requests to the poe.ninja
# site and retrieve the answer.

import requests

from database import poe_types

league_start = ""
version = "1.0"

item_types = poe_types.item_types
reward_Types = poe_types.reward_types
unique_types = poe_types.unique_types


# Method to retrieve league names. Index 0 is always the new league, while Index 1 is the old one
def get_league_names():
    api_url = "https://poe.ninja/api/data/getindexstate?"

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            api_response = response.json()

            if "economyLeagues" in api_response:
                economy_leagues = api_response["economyLeagues"]
                if economy_leagues:
                    economy_league_name = economy_leagues[0]["name"]
                else:
                    economy_league_name = None
            else:
                print("Invalid response format: Missing 'economyLeagues' key.")
                economy_league_name = None

            if "oldEconomyLeagues" in api_response:
                old_economy_leagues = api_response["oldEconomyLeagues"]
                if old_economy_leagues:
                    old_economy_league_name = old_economy_leagues[0]["name"]
                else:
                    old_economy_league_name = None
            else:
                print("Invalid response format: Missing 'oldEconomyLeagues' key.")
                old_economy_league_name = None

            return economy_league_name, old_economy_league_name

        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.RequestException as e:
        print(f"Request failed: {e}")


leagues = get_league_names()


def send_request(overview, type):
    league = leagues[0]
    api_url = f"https://poe.ninja/api/data/{overview}?league={league}&type={type}"

    try:
        # Send GET request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Save the raw response content in a variable
            api_response = response.content.decode("utf-8")
            return api_response
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.RequestException as e:
        print(f"Request failed: {e}")
