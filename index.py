import requests
import json
import re

currentLeague = 'Ancestor'

types = {
    "Currency": "currencyoverview",
    "Fragment": "currencyoverview",
    "Oil": "itemoverview",
    "Incubator": "itemoverview",
    "Scarab": "itemoverview",
    "Fossil": "itemoverview",
    "Resonator": "itemoverview",
    "Essence": "itemoverview",
    "DivinationCard": "itemoverview",
    "SkillGem": "itemoverview",
    "BaseType": "itemoverview",
    "UniqueMap": "itemoverview",
    "UniqueJewel": "itemoverview",
    "UniqueFlask": "itemoverview",
    "UniqueWeapon": "itemoverview",
    "UniqueArmour": "itemoverview",
    "UniqueAccessory": "itemoverview"
}

itemTypes = [
    'currencyitem',
    'uniqueitem',
    'gemitem',
    'rareitem',
    'magicitem',
    'whiteitem'
]

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

# Send the request and save the response in a variable
rawDivinationData = (json.loads(send_request(types['DivinationCard'], currentLeague, 'DivinationCard')))['lines']
rawCurrencyData = (json.loads(send_request(types['Currency'], currentLeague, 'Currency')))['lines']

def filter_divination_cards(cardsObject, rewardType):
    filtered_cards = []

    for card in cardsObject:
        if "explicitModifiers" in card:
            for explicitModifier in card['explicitModifiers']:
                if rewardType in explicitModifier['text']:
                    filtered_cards.append(card)

    return filtered_cards

filteredDivinationCards = filter_divination_cards(rawDivinationData, itemTypes[0])
print(filteredDivinationCards)

def compare_div_prices(filteredCards):
    price_comparison = []
    pattern = r'{(?:(\d+)x\s*)?([^}]+)}'

    for card in filteredCards:
        card_data = {}

        card_data['chaosValue'] = card['chaosValue']
        card_data['cardName'] = card['name']

        try:
            card_data['stackSize'] = card['stackSize']
        except:
            card_data['stackSize'] = 1

        if "explicitModifiers" in card:
            for explicitModifier in card['explicitModifiers']:
                match = re.search(pattern, explicitModifier['text'])

                if match:
                    card_data['amount'] = match.group(1)
                    card_data['name'] = match.group(2)
                else:
                    print("No match found")
        price_comparison.append(card_data)

    return price_comparison

print(compare_div_prices(filteredDivinationCards))
