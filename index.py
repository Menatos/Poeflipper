import os

import requests
import json
import re
import poe_types

currentLeague = 'Ancestor'

folder_name_json = 'api_responses'
folder_name_objects = 'api_objects'

itemTypes = poe_types.itemTypes
divinationTypes = poe_types.divinationTypes
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



# Send the request and save the response in a variable
rawDivinationData = (json.loads(send_request(itemTypes['DivinationCard'], currentLeague, 'DivinationCard')))['lines']
rawCurrencyData = (json.loads(send_request(itemTypes['Currency'], currentLeague, 'Currency')))['lines']


def sendRequestsAndSaveToFile():
    for itemType in itemTypes.items():
        result = send_request(itemType[1], currentLeague, itemType[0])
        folder_name = 'api_responses'
        file_path = os.path.join(folder_name, (itemType[0] + '.json'))

        if result:
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            with open(file_path, "w") as file:
                file.write(result)
        else:
            print(f"Request for {itemType} failed.")

def convertResponsesToObjects():
    for itemType in itemTypes.items():
        file_path_json = os.path.join(folder_name_json, (itemType[0] + '.json'))
        file_path_objects = os.path.join(folder_name_objects, (itemType[0] + '.json'))

        result_object = {}

        with open(file_path_json, 'r') as file:
            file_content = (json.loads(file.read()))['lines']
            for obj in file_content:

                try:
                    key = obj['name']
                    result_object[key] = obj
                except:
                    key = obj['currencyTypeName']
                    result_object[key] = obj

        with open(file_path_objects, "w") as file:
            file.write(json.dumps(result_object))




# Divination Cards
# These methods are used to filter Divination Cards
def filter_divination_cards(cardsObject, rewardType):
    filtered_cards = []

    for card in cardsObject:
        if "explicitModifiers" in card:
            for explicitModifier in card['explicitModifiers']:
                if rewardType in explicitModifier['text']:
                    filtered_cards.append(card)

    return filtered_cards

filteredDivinationCards = filter_divination_cards(rawDivinationData, divinationTypes[0])

# compare_div_prices(filteredDivinationCards)
# convertResponsesToObjects()
# sendRequestsAndSaveToFile()




# KACKDATEIEN IN DATENBANK
# FUNKTIONEN ALLLLLLLE ÜBERABEITEN WEIL BULLSHIT
# GUI
# WEITERE KATEGORIEN
# FILTER IM GUI
# Mitarbeitergespräche
