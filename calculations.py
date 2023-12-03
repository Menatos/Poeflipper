import re
import json

import index


folder_name_objects = index.folder_name_objects

# Divination Cards
# This method compares the price of a set of Divination cards compared to the value of the rewarded item.
def compare_div_prices(filteredCards):
    price_comparison = []
    pattern = r'(<currencyitem>|<uniqueitem>|<gemitem>|<rareitem>|<magicitem>|<whiteitem>)+{(?:(\d+)x\s*)?([^}]+)}'

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
                    card_data['amount'] = match.group(2)
                    card_data['name'] = match.group(3)
                else:
                    print("No match found")
        price_comparison.append(card_data)

        with open(folder_name_objects + '/Currency.json', 'r') as file:
            currency = json.loads(file.read())

        try:
            # if card_data['name'] == 'Regrading Lens' or card_data['name'] == 'Simulacrum' or  card_data['name'] == "Elderslayer's Exalted Orb" or card_data['name'] == "Incursion Vial" or card_data['name'] == "Winged Scarab" or card_data['name'] == "Delirium Orb":
            #     continue
            card_data['currencyValue'] = currency[card_data['name']]['chaosEquivalent']

            value_cards = (card_data['chaosValue'] * card_data['stackSize'])
            value_currency = int(card_data['currencyValue']) * int(card_data['amount'])
            diff = value_currency - value_cards

            if diff > 0:
                print('')
                # print("Name of Card: " + card_data['cardName'], diff, "Name of reward: " + card_data['amount'] + "x ", card_data['name'])

        except:
            print('')
            # print('Error in ' + card_data['cardName'])


    return price_comparison