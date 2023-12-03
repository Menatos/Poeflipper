import requests
import poe_types

currentLeague = 'Ancestor'

GREEN = "\033[92m"
RESET = "\033[0m"

folder_name_json = 'api_responses'
folder_name_objects = 'api_objects'

itemTypes = poe_types.itemTypes
reward_Types = poe_types.rewardTypes
uniqueTypes = poe_types.uniqueTypes

def send_request(overview ,league, type):

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

# FUNKTIONEN ALLLLLLLE ÜBERABEITEN WEIL BULLSHIT
# GUI
# WEITERE KATEGORIEN
# FILTER IM GUI
# Mitarbeitergespräche
