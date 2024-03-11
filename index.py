# This is the backbone of the application. this class is used to send api requests to the poe.ninja
# site and retrieve the answer.

import requests

import poe_types

current_league = 'Affliction'
league_start = ''

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

# WEITERE KATEGORIEN
# UNIQUE Karten Fixen bei calculate divs
# DISCORD Functions statt messages
# GEMLEVEL divcards
# Omens
# Refactor db import
# Alert bei Preisänderung
# Autopull der POB-Daten
# Regex Cluster Jewel
# Parsen der Pob Daten
# 7 Tage Daten in Db
# Vergleich aktuelle, letzte League
# Predictions für 2 Wochen basierend auf letzter league --> + Benachrichtigung bei anstieg
# https://poe.ninja/api/data/currencyhistory?league=Affliction&type=Currency&currencyId=22

# Inscribed ultimatums
