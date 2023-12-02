import requests
from enum import Enum

class type(Enum):
    Currency = "currencyoverview"
    Fragment = "currencyoverview"
    Oil = "itemoverview"
    Incubator = "itemoverview"
    Scarab = "itemoverview"
    Fossil = "itemoverview"
    Resonator = "itemoverview"
    Essence = "itemoverview"
    DivinationCard = "itemoverview"
    SkillGem = "itemoverview"
    BaseType = "itemoverview"
    UniqueMap = "itemoverview"
    UniqueJewel = "itemoverview"
    UniqueFlask = "itemoverview"
    UniqueWeapon = "itemoverview"
    UniqueArmour = "itemoverview"
    UniqueAccessory = "itemoverview"

def send_request(overview ,league, type, ):

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

# Send the request and save the response in a variable
response_data = send_request(type.DivinationCard.value, 'Ancestor', type.DivinationCard.name)

# Check if the response data is available
if response_data:
    print("API Response:")
    print(response_data)
else:
    print("No response data available.")
