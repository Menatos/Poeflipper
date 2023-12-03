import sqlite3
from pprint import pprint

from pypika import Query, Table, Field

import index

con = sqlite3.connect("poeflipper.db")
db = con.cursor()


# This method serves as a calculation method to determine the value between the cost of the Divination cards needed
# and the cost of the reward
def calculate_divination_card_difference(minProfit = 10):
    DivinationCard = Table('DivinationCard')
    Currency = Table('Currency')
    Uniques = Table('Uniques')
    Fragment = Table('Fragment')

    q = (Query
         .from_(DivinationCard)
         .join(Currency)
         .on(DivinationCard.reward == Currency.name)
         .select('name', 'chaosValue', 'stackSize', 'rewardAmount', Currency.name, Currency.chaosEquivalent)
         )
    div_cards = db.execute(str(q)).fetchall()

    for cards in div_cards:
        profit = round((cards[3] * cards[5] - cards[1] * cards[2]), 2)
        if (cards[1] * cards[2]) < (cards[3] * cards[5]) and profit >= minProfit:
            print('Name of card: ', cards[0], 'Cost of cards: ', int(cards[1]) * float(cards[2]), ' Name of reward: ', cards[4], ' Cost of reward: ', int(cards[5]), ' Amount: ', int(cards[3]))
            print(f"{index.GREEN}Profit: ", profit, f"{index.RESET}")


    # q = (Query
    #      .from_(DivinationCard)
    #      .join(Uniques)
    #      .on(DivinationCard.reward == Uniques.name)
    #      .select('*')
    #      )
    # div_cards = db.execute(str(q)).fetchall()



calculate_divination_card_difference()
