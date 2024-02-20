import sqlite3

from pypika import Query, Table

import poe_types

con = sqlite3.connect("poeflipper.db")
db = con.cursor()



# This method serves as a calculation method to determine the value between the cost of the Divination cards needed
# and the cost of the reward

def evaluate_costs(cards, price_offset, min_profit, max_profit):
    profit = round((cards[3] * cards[5] - (cards[1] * price_offset) * cards[2]), 2)
    if (cards[1] * cards[2]) < (cards[3] * cards[5]) and profit >= min_profit and profit <= max_profit:
        profitable_card = ('Name of card:', cards[0], 'Cost of cards:', int(cards[1]) * float(cards[2]), 'Name of reward:', cards[4],
        'Amount:', int(cards[3]), 'Cost of reward:', int(cards[5]))
        profit_from_card = (f"{poe_types.GREEN}Profit:", profit, f"{poe_types.RESET}")
        print(profitable_card)
        print(profit_from_card)
        # f"{cards[0]} >> {profit}c"
        return (f"{cards[0]} >> {int(cards[3])} {cards[4]} >> {profit}c")


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
             .select('name', 'chaosValue', 'corrupted', sub_table.name, getattr(sub_table, reward_cost))
             .where(main_table.listingCount > 30 and sub_table.listingCount > 30)
             .where(sub_table.gemLevel)
             )

    cards = db.execute(str(q)).fetchall()
    return cards


def calculate_divination_card_difference(min_profit=10, max_profit=5000, price_off_set=1.0, currency=True, unique=True, fragment=True, skillGem=True):
    divination_card_table = Table('DivinationCard')
    currency_table = Table('Currency')
    uniques_table = Table('Uniques')
    fragment_table = Table('Fragment')
    skillGem_table = Table('SkillGem')

    results = []

    # Currency ---------------------------------------------------------------------
    print(f'{poe_types.BLUE}CURRENCY ---------------------------------------------------------{poe_types.RESET}')
    if currency:
        currency_cards = sql_query(divination_card_table, currency_table, 'chaosEquivalent')
        for cards in currency_cards:
            result = evaluate_costs(cards, price_off_set, min_profit, max_profit)
            if result:
                results.append(result)

    # UNIQUES ---------------------------------------------------------------------
    print(f'{poe_types.BLUE}UNIQUES ----------------------------------------------------------{poe_types.RESET}')
    if unique:
        unique_cards = sql_query(divination_card_table, uniques_table, 'chaosValue', True)
        for cards in unique_cards:
            result = evaluate_costs(cards, price_off_set, min_profit, max_profit)
            if result:
                results.append(result)

    # FRAGMENT ---------------------------------------------------------------------
    print(f'{poe_types.BLUE}FRAGMENT ---------------------------------------------------------{poe_types.RESET}')
    if fragment:
        fragment_cards = sql_query(divination_card_table, fragment_table, 'chaosEquivalent')
        for cards in fragment_cards:
            result = evaluate_costs(cards, price_off_set, min_profit, max_profit)
            if result:
                results.append(result)

# SKILL GEMS -------------------------------------------------------------------------
    print(f'{poe_types.BLUE}SKILL GEMS -----------------------------------------------------{poe_types.RESET}')
    if skillGem:
        skillGem_cards = sql_query(divination_card_table, skillGem_table, 'chaosValue')
        for cards in skillGem_cards:
            result = evaluate_costs(cards, price_off_set, min_profit, max_profit)
            if result:
                results.append(result)

    return results


calculate_divination_card_difference()
