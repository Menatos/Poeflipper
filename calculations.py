import sqlite3

from pypika import Query, Table, Field

import poe_types

con = sqlite3.connect("poeflipper.db")
db = con.cursor()



# This method serves as a calculation method to determine the value between the cost of the Divination cards needed
# and the cost of the reward

def evaluate_costs(cards, priceOffSet, minProfit, maxProfit):
    profit = round((cards[3] * cards[5] - (cards[1] * priceOffSet) * cards[2]), 2)
    if (cards[1] * cards[2]) < (cards[3] * cards[5]) and profit >= minProfit and profit <= maxProfit:
        profitable_card = ('Name of card:', cards[0], 'Cost of cards:', int(cards[1]) * float(cards[2]), 'Name of reward:', cards[4],
              'Amount:', int(cards[3]), 'Cost of reward:', int(cards[5]))
        profit_from_card = (f"{poe_types.GREEN}Profit:", profit, f"{poe_types.RESET}")
        print(profitable_card)
        print(profit_from_card)
        # f"{cards[0]} >> {profit}c"
        return (f"{cards[0]} >> {int(cards[3])} {cards[4]} >> {profit}c")


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

async def calculate_divination_card_difference(minProfit = 10, maxProfit = 5000, priceOffSet=1.0 , currency=False, unique=False, fragment=False, skillGem=False):
    DivinationCard = Table('DivinationCard')
    Currency = Table('Currency')
    Uniques = Table('Uniques')
    Fragment = Table('Fragment')
    SkillGem = Table('SkillGem')

    results = []

# CURRENCY ------------------------------------------------------------------
    print(f'{poe_types.BLUE}CURRENCY ---------------------------------------------------------{poe_types.RESET}')
    if currency:
        currency_cards = sql_query(DivinationCard, Currency, 'chaosEquivalent')
        for cards in currency_cards:
            result = evaluate_costs(cards, priceOffSet, minProfit, maxProfit)
            if result:
                results.append(result)

# UNIQUES ---------------------------------------------------------------------
    print(f'{poe_types.BLUE}UNIQUES ----------------------------------------------------------{poe_types.RESET}')
    if unique:
        unique_cards = sql_query(DivinationCard, Uniques, 'chaosValue', True)
        for cards in unique_cards:
            result = evaluate_costs(cards, priceOffSet, minProfit, maxProfit)
            if result:
                results.append(result)

# FRAGMENT ---------------------------------------------------------------------
    print(f'{poe_types.BLUE}FRAGMENT ---------------------------------------------------------{poe_types.RESET}')
    if fragment:
        fragment_cards = sql_query(DivinationCard, Fragment, 'chaosEquivalent')
        for cards in fragment_cards:
            result = evaluate_costs(cards, priceOffSet, minProfit, maxProfit)
            if result:
                results.append(result)

    return results

# # SKILL GEMS -------------------------------------------------------------------------
#     print(f'{poe_types.BLUE}SKILL GEMS -----------------------------------------------------{poe_types.RESET}')
#     if skillGem:


calculate_divination_card_difference
