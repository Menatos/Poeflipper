# This file takes care of importing all the poe ninja data into a sqlite3 database.
# Value mapping is also done in this file.

import json
import re
import sqlite3

# https://pypika.readthedocs.io/en/latest/2_tutorial.html
from pypika import Query, Table

import index
import poe_types

con = sqlite3.connect("poeflipper.db")
db = con.cursor()
ItemList = "ItemList"

item_types = poe_types.item_types
reward_types = poe_types.reward_types
unique_types = poe_types.unique_types
table_specs = poe_types.table_specs


def is_field_present(table_spec, table_name, field_name):
    if table_spec["name"] == table_name:
        return any(field["name"] == field_name for field in table_spec["fields"])
    return False


def create_db_tables():
    def generate_field_string(fields):
        field_string = ", ".join(f"{field['name']} {field['type']}" for field in fields)
        return field_string

    for table_spec in table_specs:
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_spec['name']}({generate_field_string(table_spec['fields'])})"
        db.execute(create_table_query)

    # https://docs.python.org/3/library/sqlite3.html
    # q = Query.from_('movie').select('name', 'year', 'score')
    #
    # con = sqlite3.connect("tutorial.db")
    # cur = con.cursor()
    # res = cur.execute(str(q))
    #
    # print(res.fetchall())


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
        "mapTier": obj.get("mapTier", 1),
        "gemLevel": obj.get("gemLevel", 0),
        "quality": obj.get("gemQuality", 0),
        "corrupted": 1 if "corrupted" in obj else 0,
        "variant": obj.get("variant", ""),
        "rewardType": "",
        "rewardAmount": "",
        "reward": "",
        "receiveSparkLine": obj.get("receiveSparkLine", 0),
        "paySparkLine": obj.get("paySparkLine", 0),
        "sparkline": obj.get("sparkline", 0),
        "detailsId": obj.get("detailsId", "")
    }

    # Match DivinationCard rewards to db fields
    if type == "DivinationCard" and "explicitModifiers" in obj:
        pattern = r"<(currencyitem|uniqueitem|gemitem|rareitem|magicitem|whiteitem|divination)+>\s*{(?:(\d+)x\s*)?(?:((Level\s+)(\d+)(\s)+))*([^}]+)}"

        for explicit_modifier in obj["explicitModifiers"]:
            match = re.search(pattern, explicit_modifier.get("text", ""))

            if match:
                field_mapping["rewardType"] = match.group(1)
                field_mapping["rewardAmount"] = match.group(2) or 1
                field_mapping["reward"] = match.group(7)
                field_mapping["gemLevel"] = match.group(5) or 1
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


def insert_into_db(response, table_spec, table_name, current_table, item_list_table):
    for obj in response:
        values = map_values(obj, table_name)

        values_mapped = []

        # Build the query dynamically based on the table specification
        for value in values:
            if is_field_present(table_spec, table_name, value):
                values_mapped.append(str(values[value]))

        q = Query.into(current_table).insert(values_mapped)

        q_index = Query.into(item_list_table).insert(
            values["id"], values["name"], table_name
        )

        # Do not import relic uniques, they throw off the values
        if values.get("detailsId") and "relic" in values.get("detailsId"):
            continue

        # Execute the queries
        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(
            f"{table_name} Itemname: {values['name']} ID: {values['id']} import complete"
        )


def refresh_db_values():
    # Delete all records from ItemList
    db.execute(f"DELETE FROM {ItemList}")
    item_list_table = Table(ItemList)

    # Iterate over table specifications excluding ItemList
    for table_spec in [t for t in table_specs if t["name"] != "ItemList"]:
        table_name = table_spec["name"]

        # Delete all records from the current table
        current_table = Table(table_name)
        db.execute(f"DELETE FROM {table_name}")

        # Unique Table is joined instead of separate, separate queries get merged
        if table_name.startswith("Uniques"):
            for unique_type in unique_types:
                response = json.loads(
                    index.send_request(
                        unique_types[unique_type], index.current_league, unique_type
                    )
                )["lines"]
                insert_into_db(
                    response, table_spec, table_name, current_table, item_list_table
                )
        else:
            response = json.loads(
                index.send_request(
                    item_types[table_name],
                    index.current_league,
                    table_name,
                )
            )["lines"]

        insert_into_db(response, table_spec, table_name, current_table, item_list_table)


# create_db_tables()
# refresh_db_values()
