import sqlite3
from pprint import pprint

from pypika import Query, Table, Field

import index

con = sqlite3.connect("poeflipper.db")
db = con.cursor()


# This method serves as a calculation method to determine the value between the cost of the Divination cards needed
# and the cost of the reward

def evaluate_costs(cards, priceOffSet, minProfit, maxProfit):
    profit = round((cards[3] * cards[5] - (cards[1] * priceOffSet) * cards[2]), 2)
    if (cards[1] * cards[2]) < (cards[3] * cards[5]) and profit >= minProfit and profit <= maxProfit:
        print('Name of card:', cards[0], 'Cost of cards:', int(cards[1]) * float(cards[2]), 'Name of reward:', cards[4],
              'Amount:', int(cards[3]), 'Cost of reward:', int(cards[5]))
        print(f"{index.GREEN}Profit:", profit, f"{index.RESET}")


def sql_query(mainTable, subTable, rewardCost, low_confidence=False, skillGem=False):
    q = (Query
         .from_(mainTable)
         .join(subTable)
         .on(mainTable.reward == subTable.name)
         .select('name', 'chaosValue', 'stackSize', 'rewardAmount', subTable.name, getattr(subTable, rewardCost))
         )
    if low_confidence:
        q = (Query
             .from_(mainTable)
             .join(subTable)
             .on(mainTable.reward == subTable.name)
             .select('name', 'chaosValue', 'stackSize', 'rewardAmount', subTable.name, getattr(subTable, rewardCost))
             .where(mainTable.listingCount > 30 and subTable.listingCount > 30)
             )
    if skillGem:
        q = (Query
             .from_(mainTable)
             .join(subTable)
             .on(mainTable.reward == subTable.name)
             .select('name', 'chaosValue', 'stackSize', 'rewardAmount', subTable.name, getattr(subTable, rewardCost))
             .where(mainTable.listingCount > 30 and subTable.listingCount > 30)
             .where(subTable.gemLevel)
             )

    cards = db.execute(str(q)).fetchall()
    return cards

def calculate_divination_card_difference(minProfit = 10, maxProfit = 5000, priceOffSet=1.0 , currency=True, unique=True, fragment=True, skillGem=False):
    DivinationCard = Table('DivinationCard')
    Currency = Table('Currency')
    Uniques = Table('Uniques')
    Fragment = Table('Fragment')
    SkillGem = Table('SkillGem')

# CURRENCY ------------------------------------------------------------------
    print(f'{index.BLUE}CURRENCY ---------------------------------------------------------{index.RESET}')
    if currency:
        currency_cards = sql_query(DivinationCard, Currency, 'chaosEquivalent')
        for cards in currency_cards:
            evaluate_costs(cards, priceOffSet, minProfit, maxProfit)

# UNIQUES ---------------------------------------------------------------------
    print(f'{index.BLUE}UNIQUES ----------------------------------------------------------{index.RESET}')
    if unique:
        unique_cards = sql_query(DivinationCard, Uniques, 'chaosValue', True)
        for cards in unique_cards:
            evaluate_costs(cards, priceOffSet, minProfit, maxProfit)

# FRAGMENT ---------------------------------------------------------------------
    print(f'{index.BLUE}FRAGMENT ---------------------------------------------------------{index.RESET}')
    if fragment:
        fragment_cards = sql_query(DivinationCard, Fragment, 'chaosEquivalent')
        for cards in fragment_cards:
            evaluate_costs(cards, priceOffSet, minProfit, maxProfit)

# # SKILL GEMS -------------------------------------------------------------------------
#     print(f'{index.BLUE}SKILL GEMS -----------------------------------------------------{index.RESET}')
#     if skillGem:


calculate_divination_card_difference()
