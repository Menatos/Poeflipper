import json
import re
import sqlite3

# Import PyPika for building SQL queries
from pypika import Query, Table, Parameter

# Import custom modules
import index
from database import poe_types
import helpers.last_run as lr

# Connect to the SQLite database
con = sqlite3.connect("../poeflipper.db")
db = con.cursor()
ItemList = "ItemList"
PriceHistory = "PriceHistory"

# Define item types, reward types, unique types, and table specifications
item_types = poe_types.item_types
item_history = poe_types.item_history
reward_types = poe_types.reward_types
unique_types = poe_types.unique_types
table_specs = poe_types.table_specs
misc_table_specs = poe_types.misc_table_specs

item_list_table = Table(ItemList)
price_history_table = Table(PriceHistory)

leagues = index.leagues

# Check if a field is present in a given table specification
def is_field_present(table_spec, table_name, field_name):
    if table_spec["name"] == table_name:
        return any(field["name"] == field_name for field in table_spec["fields"])
    return False


# Create database tables based on predefined specifications
def create_db_tables():
    def generate_field_string(table_spec):
        fields = table_spec["fields"]

        field_string = ", ".join(f"{field['name']} {field['type']} {field.get('primary_key', '')}" for field in fields)
        return field_string

    def create_table(table_spec):
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_spec['name']}({generate_field_string(table_spec)})"
        print(create_table_query)
        db.execute(create_table_query)

    # Iterate over table specifications and create tables
    for table_spec in table_specs:
        create_table(table_spec)
    # Create misc_tables
    for table_spec in misc_table_specs:
        create_table(table_spec)

# Map values from the received JSON object to the corresponding fields in the database
def map_values(obj, type=""):
    superior_gems = ["Enlighten", "Enhance", "Empower"]

    field_mapping = {
        "id": obj.get("id", 0),
        "name": obj.get("name", obj.get("currencyTypeName", "")),
        "icon": obj.get("icon", ""),
        "levelRequired": obj.get("levelRequired", 0),
        "baseType": obj.get("baseType", ""),
        "itemClass": obj.get("itemClass", ""),
        "itemType": obj.get("itemType", ""),
        "chaosValue": obj.get("chaosValue", 0),
        "chaosEquivalent": obj.get("chaosEquivalent", 0),
        "listingCount": obj.get("listingCount", 0),
        "stackSize": obj.get("stackSize", 1),
        "count": obj.get("count", 0),
        "mapTier": obj.get("mapTier", 0),
        "gemLevel": obj.get("gemLevel", 1),
        "quality": obj.get("gemQuality", 0),
        "corrupted": 1 if "corrupted" in obj else 0,
        "variant": obj.get("variant", ""),
        "rewardType": "",
        "rewardAmount": "",
        "reward": "",
        "links": obj.get("links", 0),
        "receiveSparkLine": obj.get("receiveSparkLine", 0),
        "paySparkLine": obj.get("paySparkLine", 0),
        "sparkline": obj.get("sparkline", 0),
        "detailsId": obj.get("detailsId", ""),
    }

    # Match DivinationCard rewards to db fields
    if type == "DivinationCard" and "explicitModifiers" in obj:
        pattern = r"<(\w+item|divination)+>\s*{(?:(\d+)x\s*)?(?:Level\s+(\d+)\s+)*([^}]+)}(?:.*{Map Tier:}.*{(\d+)})*"

        for explicit_modifier in obj["explicitModifiers"]:
            string = explicit_modifier.get("text", "").replace("\n", "")
            match = re.search(pattern, string)

            if match:
                field_mapping["rewardType"] = match.group(1)
                field_mapping["rewardAmount"] = match.group(2) or 1
                field_mapping["reward"] = match.group(4)
                field_mapping["gemLevel"] = match.group(3) or 1
                field_mapping["mapTier"] = match.group(5) or 0
            if field_mapping["reward"] in superior_gems:
                field_mapping["reward"] = field_mapping["reward"] + " Support"

            # Check for the presence of "corrupted" in the text
            if "<corrupted>" in explicit_modifier.get("text", ""):
                field_mapping["corrupted"] = 1
            else:
                field_mapping["corrupted"] = 0

            # Extract amount of quality, default to 0 if not present
            quality_match = re.search(
                r"<default>{Quality:}\s*<augmented>{\+(\d+)%}",
                explicit_modifier.get("text", ""),
            )
            field_mapping["quality"] = (
                int(quality_match.group(1)) if quality_match else 0
            )

    return field_mapping


# Insert values into the database tables based on the received response and table specifications
def insert_into_db(response, table_spec, table_name, current_table, item_list_table, item_type=None):
    for obj in response["lines"]:
        values = map_values(obj, table_name)
        values_mapped = []

        if table_name == "Currency" or table_name == "Fragment":
            filtered_item_values = list(filter(lambda item: item['name'] == values["name"], response["currencyDetails"]))[0]

            item_id = int(filtered_item_values["id"])
            name = str(filtered_item_values["name"])
            icon = str(filtered_item_values["icon"])

            values["id"] = item_id
            values["name"] = name
            values["icon"] = icon

        # Build the query dynamically based on the table specification
        for value in values:
            if is_field_present(table_spec, table_name, value):
                values_mapped.append(str(values[value]))

        q = Query.into(current_table).insert(values_mapped)

        q_index = Query.into(item_list_table).insert(
            values["id"], values["name"], table_name, item_type
        )

        q_price = Query.into(price_history_table).insert(values["id"], values['name'], None, None)

        # Do not import relic uniques, they throw off the values
        if values.get("detailsId") and "relic" in values.get("detailsId"):
            continue

        # Execute the queries
        db.execute(str(q))
        db.execute(str(q_index))

        item_in_price_history = db.execute(f"SELECT id FROM {price_history_table} WHERE id = {values['id']}").fetchone()

        if not item_in_price_history:
            db.execute(str(q_price))

        con.commit()
        print(
            f"{table_name} Itemname: {values['name']} ID: {values['id']} import complete"
        )


# Refresh values in the database by deleting records and importing new ones
def refresh_db_values():
    # Delete all records from ItemList
    db.execute(f"DELETE FROM {ItemList}")

    # Iterate over table specifications excluding ItemList
    for table_spec in table_specs:
        table_name = table_spec["name"]

        # Delete all records from the current table
        current_table = Table(table_name)
        db.execute(f"DELETE FROM {table_name}")

        # Unique Table is joined instead of separate, separate queries get merged
        if table_name.startswith("Uniques"):
            for unique_type in unique_types:
                response = json.loads(
                    index.send_request(unique_types[unique_type], unique_type)
                )
                insert_into_db(
                    response, table_spec, table_name, current_table, item_list_table, unique_type
                )
        else:
            response = json.loads(
                index.send_request(
                    item_types[table_name],
                    table_name,
                )
            )
            insert_into_db(response, table_spec, table_name, current_table, item_list_table)

    lr.save_last_run_time_stamp(prefix="refresh_db_values")
    return


def insert_price_history(response="", league=leagues[0]):

    ids = []

    if response:
        ids = [x[0] for x in response]

    q = (
        Query.from_(item_list_table)
        .left_join(price_history_table)
        .on(item_list_table.id == price_history_table.id)
        .select('*')
        .where(item_list_table.table_name != "BaseType")
        .where(item_list_table.id.isin(ids))
        .groupby(item_list_table.id)
    )

    item_values = db.execute(str(q)).fetchall()

    for value in item_values:

        item_id = value[0]
        item_name = value[1]
        item_table = value[2]
        if value[3]:
            item_type = value[3]
        else:
            item_type = item_table
        old_league_prices = value[6]
        new_league_prices = value[7]

        if old_league_prices and league == leagues[1]:
            print(f"Skipping {item_name} as it already has old league prices")
            continue
        elif new_league_prices and league == leagues[0]:
            print(f"Skipping {item_name} as it already has new league prices")
            continue

        print(item_history[item_table], league, item_type, item_id)

        price_history = index.send_price_history_request(item_history[item_table], league, item_type, item_id)

        if price_history:
            if league == leagues[0]:
                league_prices = price_history_table.new_league_prices
            else:
                league_prices = price_history_table.old_league_prices

            q = Query.update(price_history_table).set(league_prices, str(price_history)).where(price_history_table.id == item_id and price_history_table.name == item_name)

            print(f"Inserting price history..... Item: {item_name} ID: {item_id} Table: {item_table} Type: {item_type} League: {league}")
            db.execute(str(q))
            con.commit()

    lr.save_last_run_time_stamp(prefix="price_history")
    return


def refresh_price_history(item_name="", league=leagues[1]):
    q = (
        Query.from_(item_list_table)
        .select('*')
        .where(item_list_table.table_name != "BaseType")
    )

    if item_name:

        q = q.where(item_list_table.name. like(Parameter('?')))

        response = db.execute(str(q), (item_name,)).fetchall()
        insert_price_history(response, league)
    else:
        response = db.execute(str(q)).fetchall()
        insert_price_history(response, league)


def refresh_old_league_prices():
    refresh_price_history(league=leagues[1])

# Create database tables and refresh values
# create_db_tables()
# refresh_db_values()
# refresh_price_history()
