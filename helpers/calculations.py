import json
import sqlite3
from pprint import pprint

from pypika import Query, Table
from database import poe_types

# Establish a connection to the SQLite database
con = sqlite3.connect("../poeflipper.db")
db = con.cursor()


# This method serves as a calculation method to determine the value between the cost of the Divination cards needed
# and the cost of the reward
def evaluate_costs(cards, price_offset, min_profit, max_profit, card_type=""):
    # Unpack card information
    card_name = cards[0]
    card_amount = int(cards[2])
    card_value = float(cards[1])
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
        if profit / card_amount >= 50:
            return f"> {card_name} > {card_amount} cards > {reward_amount} {reward_name} > Profit: __***{profit}c***__"
        if profit / card_amount >= 25:
            return f"> {card_name} > {card_amount} cards > {reward_amount} {reward_name} > Profit: ***{profit}c***"
        else:
            return f"> {card_name} > {card_amount} cards > {reward_amount} {reward_name} > Profit: {profit}c"


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
            main_table.name,
            "chaosValue",
            "stackSize",
            "rewardAmount",
            sub_table.name,
            getattr(sub_table, reward_cost),
        )
        .groupby(main_table.name)
    )

    if "Uniques" in str(sub_table):
        q = q.where(sub_table.links == 0)
        q = q.where(main_table.mapTier == sub_table.mapTier)

    # Add additional conditions based on parameters
    if low_confidence:
        q = q.where(main_table.listingCount > 30 and sub_table.listingCount > 30)

    if skill_gem:
        q = q.where(main_table.gemLevel == sub_table.gemLevel)
        q = q.where(main_table.quality == sub_table.quality)
        q = q.where(main_table.corrupted == sub_table.corrupted)

    # Execute the query and fetch results
    cards = db.execute(str(q)).fetchall()
    cards = sorted(cards, key=lambda x: x[1], reverse=True)

    return cards


# Main method to calculate differences in divination card values
def calculate_divination_card_difference(
    min_profit=10,
    max_profit=5000,
    price_off_set=1.0,
    Currency=False,
    Unique=False,
    Fragment=False,
    SkillGem=False,
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
    if Currency:
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
    if Unique:
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
    if Fragment:
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
    if SkillGem:
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


def calculate_price_change(price_change=30):
    table_specs = poe_types.table_specs
    price_changes = {}

    for table_spec in [
        t for t in table_specs if t["name"] != "ItemList" and t["name"] != "BaseType"
    ]:
        table_name = table_spec["name"]
        current_table = Table(table_name)
        price_changes[table_name] = []

        # Create a query using the PyPika library
        q = (
            Query.from_(current_table)
            .select("name", "chaosValue", "sparkline")
            .where(current_table.listingCount >= 50)
        )

        if table_name == "Currency" or table_name == "Fragment":
            q = (
                Query.from_(current_table)
                .select("name", "chaosEquivalent", "paySparkline")
                .where(current_table.listingCount >= 200)
            )

        q = q.groupby("name")

        # Execute the query and fetch results
        data = db.execute(str(q)).fetchall()

        for item in data:
            name = item[0]
            value = item[1]
            sparkline = json.loads(item[2].replace("'", '"').replace("None", "0"))
            total_change = sparkline["totalChange"]

            if (
                total_change >= price_change or total_change <= -price_change
            ) and value >= 10:
                price_changes[table_name].append(
                    {
                        "name": name,
                        "value": value,
                        "total_change": total_change,
                        "type": table_name,
                    }
                )

        price_changes[table_name] = sorted(
            price_changes[table_name],
            key=lambda x: (x["total_change"], x["value"]),
            reverse=True,
        )

    return price_changes


# Run the main function
# calculate_divination_card_difference()
# calculate_divination_card_difference(Currency=True)
# calculate_price_change()

# 10 kennen
# hintergrundgeschichte
# wortlaut kurzversion
