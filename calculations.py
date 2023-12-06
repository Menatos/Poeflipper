import sqlite3
from pprint import pprint

from pypika import Query, Table, Field

import index

con = sqlite3.connect("poeflipper.db")
db = con.cursor()


# This method serves as a calculation method to determine the value between the cost of the Divination cards needed
# and the cost of the reward

def evaluate_costs(cards, price_offset, min_profit, max_profit):
    profit = round((cards[3] * cards[5] - (cards[1] * price_offset) * cards[2]), 2)
    if (cards[3] * cards[5]) > (cards[1] * cards[2]) <= profit <= max_profit:
        print('Name of card:', cards[0], 'Cost of cards:', int(cards[1]) * float(cards[2]), 'Name of reward:', cards[4],
              'Amount:', int(cards[3]), 'Cost of reward:', int(cards[5]))
        print(f"{index.GREEN}Profit:", profit, f"{index.RESET}")


def sql_query(main_table, sub_table, reward_cost, low_confidence=False, skill_gem=False):
    q = (Query
         .from_(main_table)
         .join(sub_table)
         .on(main_table.reward == sub_table.name)
         .select('name', 'chaosValue', 'stackSize', 'rewardAmount', sub_table.name, getattr(sub_table, reward_cost))
         )
    if low_confidence:
        q = (Query
             .from_(main_table)
             .join(sub_table)
             .on(main_table.reward == sub_table.name)
             .select('name', 'chaosValue', 'stackSize', 'rewardAmount', sub_table.name, getattr(sub_table, reward_cost))
             .where(main_table.listingCount > 30 and sub_table.listingCount > 30)
             )
    if skill_gem:
        q = (Query
             .from_(main_table)
             .join(sub_table)
             .on(main_table.reward == sub_table.name)
             .select('name', 'chaosValue', 'stackSize', 'rewardAmount', sub_table.name, getattr(sub_table, reward_cost))
             .where(main_table.listingCount > 30 and sub_table.listingCount > 30)
             .where(sub_table.gemLevel)
             )

    cards = db.execute(str(q)).fetchall()
    return cards


def calculate_divination_card_difference(min_profit=10, max_profit=5000, price_off_set=1.0, currency=True, unique=True,
                                         fragment=True, skill_gem=False):
    divination_card = Table('DivinationCard')
    currency = Table('Currency')
    uniques = Table('Uniques')
    fragment = Table('Fragment')
    skill_gem = Table('SkillGem')

    # CURRENCY ------------------------------------------------------------------
    print(f'{index.BLUE}CURRENCY ---------------------------------------------------------{index.RESET}')
    if currency:
        currency_cards = sql_query(divination_card, currency, 'chaosEquivalent')
        for cards in currency_cards:
            evaluate_costs(cards, price_off_set, min_profit, max_profit)

    # UNIQUES ---------------------------------------------------------------------
    print(f'{index.BLUE}UNIQUES ----------------------------------------------------------{index.RESET}')
    if unique:
        unique_cards = sql_query(divination_card, uniques, 'chaosValue', True)
        for cards in unique_cards:
            evaluate_costs(cards, price_off_set, min_profit, max_profit)

    # FRAGMENT ---------------------------------------------------------------------
    print(f'{index.BLUE}FRAGMENT ---------------------------------------------------------{index.RESET}')
    if fragment:
        fragment_cards = sql_query(divination_card, fragment, 'chaosEquivalent')
        for cards in fragment_cards:
            evaluate_costs(cards, price_off_set, min_profit, max_profit)


# # SKILL GEMS -------------------------------------------------------------------------
#     print(f'{index.BLUE}SKILL GEMS -----------------------------------------------------{index.RESET}')
#     if skillGem:


calculate_divination_card_difference()
