import sqlite3
from pypika import Query, Table
import poe_types

# Establish a connection to the SQLite database
con = sqlite3.connect("poeflipper.db")
db = con.cursor()


# This method serves as a calculation method to determine the value between the cost of the Divination cards needed
# and the cost of the reward
def evaluate_costs(cards, price_offset, min_profit, max_profit, card_type=""):
    # Unpack card information
    card_name = cards[0]
    card_amount = int(cards[1])
    card_value = float(cards[2])
    card_cost = card_amount * price_offset * card_value
    reward_name = cards[4]
    reward_amount = int(cards[3])
    reward_value = float(cards[5])

    # Calculate profit
    profit = round(((reward_amount * reward_value) - (card_cost)), 2)

    # Check if the card is profitable within the specified profit range
    if (card_amount * card_value) < (
        reward_amount * reward_value
    ) and min_profit <= profit <= max_profit:
        # Display information about the profitable card
        profitable_card = (
            "Name of card:",
            card_name,
            "Cost of cards:",
            card_cost,
            "Name of reward:",
            reward_name,
            "Amount:",
            reward_amount,
            "Cost of reward:",
            reward_value,
        )
        profit_from_card = (f"{poe_types.GREEN}Profit:", profit, f"{poe_types.RESET}")
        print(profitable_card)
        print(profit_from_card)
        return f"{card_name} >> {int(cards[3])} {cards[4]} >> {profit}c"


# Method to perform SQL queries
def sql_query(
    main_table, sub_table, reward_cost, low_confidence=False, skill_gem=False
):
    # Create a query using the PyPika library
    q = (
        Query.from_(main_table)
        .join(sub_table)
        .on(main_table.reward == sub_table.name)
        .select(
            "name",
            "chaosValue",
            "stackSize",
            "rewardAmount",
            sub_table.name,
            getattr(sub_table, reward_cost),
        )
    )

    # Add additional conditions based on parameters
    if low_confidence:
        q = (
            Query.from_(main_table)
            .join(sub_table)
            .on(main_table.reward == sub_table.name)
            .select(
                "name",
                "chaosValue",
                "stackSize",
                "rewardAmount",
                sub_table.name,
                getattr(sub_table, reward_cost),
            )
            .where(main_table.listingCount > 30 and sub_table.listingCount > 30)
        )
    elif skill_gem:
        q = (
            Query.from_(main_table)
            .join(sub_table)
            .on(main_table.reward == sub_table.name)
            .select(
                "name",
                "chaosValue",
                "stackSize",
                "rewardAmount",
                sub_table.name,
                getattr(sub_table, reward_cost),
            )
            .where(main_table.gemLevel == sub_table.gemLevel)
            .where(main_table.quality == sub_table.quality)
            .where(main_table.corrupted == sub_table.corrupted)
        )

    # Execute the query and fetch results
    cards = db.execute(str(q)).fetchall()
    return cards


# Main method to calculate differences in divination card values
def calculate_divination_card_difference(
    min_profit=10,
    max_profit=5000,
    price_off_set=1.0,
    currency=True,
    unique=True,
    fragment=True,
    skillGem=True,
):
    divination_card_table = Table("DivinationCard")
    currency_table = Table("Currency")
    uniques_table = Table("Uniques")
    fragment_table = Table("Fragment")
    skillGem_table = Table("SkillGem")

    results = []

    # Currency
    print(
        f"{poe_types.BLUE}CURRENCY ---------------------------------------------------------{poe_types.RESET}"
    )
    if currency:
        currency_cards = sql_query(
            divination_card_table, currency_table, "chaosEquivalent"
        )
        for cards in currency_cards:
            result = evaluate_costs(cards, price_off_set, min_profit, max_profit)
            if result:
                results.append(result)

    # Uniques
    print(
        f"{poe_types.BLUE}UNIQUES ----------------------------------------------------------{poe_types.RESET}"
    )
    if unique:
        unique_cards = sql_query(
            divination_card_table, uniques_table, "chaosValue", True
        )
        for cards in unique_cards:
            result = evaluate_costs(cards, price_off_set, min_profit, max_profit)
            if result:
                results.append(result)

    # Fragment
    print(
        f"{poe_types.BLUE}FRAGMENT ---------------------------------------------------------{poe_types.RESET}"
    )
    if fragment:
        fragment_cards = sql_query(
            divination_card_table, fragment_table, "chaosEquivalent"
        )
        for cards in fragment_cards:
            result = evaluate_costs(cards, price_off_set, min_profit, max_profit)
            if result:
                results.append(result)

    # Skill Gems
    print(
        f"{poe_types.BLUE}SKILL GEMS -----------------------------------------------------{poe_types.RESET}"
    )
    if skillGem:
        card_type = "skillGem"
        skillGem_cards = sql_query(
            divination_card_table, skillGem_table, "chaosValue", False, True
        )
        for cards in skillGem_cards:
            result = evaluate_costs(
                cards, price_off_set, min_profit, max_profit, card_type
            )
            if result:
                results.append(result)

    return results


# Run the main function
calculate_divination_card_difference()
