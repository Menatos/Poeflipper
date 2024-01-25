# This file takes care of importing all the poe ninja data into a sqlite3 database.
# Value mapping is also done in this file.

import json
import re
import sqlite3

# https://pypika.readthedocs.io/en/latest/2_tutorial.html
from pypika import Query, Table, Field

import index
import poe_types



con = sqlite3.connect("poeflipper.db")
db = con.cursor()
ItemList = 'ItemList'

item_types = poe_types.item_types
reward_types = poe_types.reward_types
unique_types = poe_types.unique_types
table_specs = poe_types.table_specs


def create_db_tables():

    def generate_field_string(fields):
        field_string = ', '.join(f"{field['name']} {field['type']}" for field in fields)
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



def map_values(obj, type=''):
    field_mapping = {
        'id': 0,
        'name': obj.get('name', ''),
        'icon': obj.get('icon', ''),
        'levelRequired': obj.get('levelRequired', 0),
        'baseType': obj.get('baseType', ''),
        'itemClass': obj.get('itemClass', ''),
        'itemType': obj.get('itemType', ''),
        'chaosValue': obj.get('chaosValue', obj.get('chaosEquivalent', 0)),
        'listingCount': obj.get('listingCount', 0),
        'stackSize': obj.get('stackSize', 1),
        'count': obj.get('count', 0),
        'mapTier': obj.get('mapTier', 1),
        'gemLevel': obj.get('gemLevel', 0),
        'gemQuality': obj.get('gemQuality', 0),
        'corrupted': 1 if 'corrupted' in obj else 0,
        'variant': obj.get('variant', ''),
        'rewardType': '',
        'rewardAmount': '1',
        'reward': ''
    }

    if type == 'DivinationCard' and 'explicitModifiers' in obj:
        pattern = r'<(currencyitem|uniqueitem|gemitem|rareitem|magicitem|whiteitem|divination)+>\s*{(?:(\d+)x\s*)?([^}]+)}'

        for explicit_modifier in obj['explicitModifiers']:
            match = re.search(pattern, explicit_modifier.get('text', ''))

            if match:
                field_mapping['rewardType'] = match.group(1)
                field_mapping['rewardAmount'] = match.group(2) or '1'
                field_mapping['reward'] = match.group(3)

    return field_mapping


def refresh_db_values():
    db.execute(f'DELETE FROM {ItemList}')
    item_list_table = Table(ItemList)

    # BASETYPE TABLE --------------------------------------------------
    table_name = 'BaseType'
    response = (json.loads(index.send_request(item_types[table_name], index.current_league, table_name)))['lines']

    base_type = Table(table_name)
    db.execute(f'DELETE FROM {table_name}')

    for obj in response:
        value = map_values(obj)

        q = Query.into(base_type).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['levelRequired'],
            value['baseType'],
            value['itemClass'],
            value['chaosValue'],
            value['listingCount'],
            value['variant'],
        )

        q_index = Query.into(item_list_table).insert(
            value['id'],
            value['name'],
            table_name
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{table_name} Itemname: {value['name']} ID: {value['id']} import complete")

    # CURRENCY TABLE --------------------------------------------------
    table_name = 'Currency'
    response = (json.loads(index.send_request(item_types[table_name], index.current_league, table_name)))['lines']

    base_type = Table(table_name)
    db.execute(f'DELETE FROM {table_name}')

    for obj in response:
        value = map_values(obj)

        q = Query.into(base_type).insert(
            value['name'],
            value['icon'],
            value['chaosValue'],
        )

        q_index = Query.into(item_list_table).insert(
            '',
            value['name'],
            table_name
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{table_name} Itemname: {value['name']} import complete")

    # DIVINATIONCARD TABLE --------------------------------------------------
    table_name = 'DivinationCard'
    response = (json.loads(index.send_request(item_types[table_name], index.current_league, table_name)))['lines']

    base_type = Table(table_name)
    db.execute(f'DELETE FROM {table_name}')

    for obj in response:
        value = map_values(obj, 'DivinationCard')

        q = Query.into(base_type).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['stackSize'],
            value['reward'],
            value['rewardAmount'],
            value['rewardType'],
            value['chaosValue'],
            value['count'],
            value['listingCount']
        )

        q_index = Query.into(item_list_table).insert(
            value['id'],
            value['name'],
            table_name
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{table_name} Itemname: {value['name']} ID: {value['id']} import complete")

    # ESSENCE TABLE --------------------------------------------------
    table_name = 'Essence'
    response = (json.loads(index.send_request(item_types[table_name], index.current_league, table_name)))['lines']

    base_type = Table(table_name)
    db.execute(f'DELETE FROM {table_name}')

    for obj in response:
        value = map_values(obj)

        q = Query.into(base_type).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['mapTier'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(item_list_table).insert(
            value['id'],
            value['name'],
            table_name
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{table_name} Itemname: {value['name']} ID: {value['id']} import complete")

    # FOSSIL TABLE --------------------------------------------------
    table_name = 'Fossil'
    response = (json.loads(index.send_request(item_types[table_name], index.current_league, table_name)))['lines']

    base_type = Table(table_name)
    db.execute(f'DELETE FROM {table_name}')

    for obj in response:
        value = map_values(obj)

        q = Query.into(base_type).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(item_list_table).insert(
            value['id'],
            value['name'],
            table_name
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{table_name} Itemname: {value['name']} ID: {value['id']} import complete")

    # FRAGMENT TABLE --------------------------------------------------
    table_name = 'Fragment'
    response = (json.loads(index.send_request(item_types[table_name], index.current_league, table_name)))['lines']

    base_type = Table(table_name)
    db.execute(f'DELETE FROM {table_name}')

    for obj in response:
        value = map_values(obj)

        q = Query.into(base_type).insert(
            value['name'],
            value['icon'],
            value['chaosValue'],
        )

        q_index = Query.into(item_list_table).insert(
            '',
            value['name'],
            table_name
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{table_name} Itemname: {value['name']} import complete")

    # INCUBATOR TABLE --------------------------------------------------
    table_name = 'Incubator'
    response = (json.loads(index.send_request(item_types[table_name], index.current_league, table_name)))['lines']

    base_type = Table(table_name)
    db.execute(f'DELETE FROM {table_name}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(base_type).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(item_list_table).insert(
            value['id'],
            value['name'],
            table_name
        )

        db.execute(str(q))
        db.execute(str(q_index))

        con.commit()
        print(f"{table_name} Itemname: {value['name']} ID: {value['id']} import complete")

    # OIL TABLE --------------------------------------------------
    table_name = 'Oil'
    response = (json.loads(index.send_request(item_types[table_name], index.current_league, table_name)))['lines']

    base_type = Table(table_name)
    db.execute(f'DELETE FROM {table_name}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(base_type).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(item_list_table).insert(
            value['id'],
            value['name'],
            table_name
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{table_name} Itemname: {value['name']} ID: {value['id']} import complete")

    # RESONATOR TABLE --------------------------------------------------
    table_name = 'Resonator'
    response = (json.loads(index.send_request(item_types[table_name], index.current_league, table_name)))['lines']

    base_type = Table(table_name)
    db.execute(f'DELETE FROM {table_name}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(base_type).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(item_list_table).insert(
            value['id'],
            value['name'],
            table_name
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{table_name} Itemname: {value['name']} ID: {value['id']} import complete")

    # SCARAB TABLE --------------------------------------------------
    table_name = 'Scarab'
    response = (json.loads(index.send_request(item_types[table_name], index.current_league, table_name)))['lines']

    base_type = Table(table_name)
    db.execute(f'DELETE FROM {table_name}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(base_type).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(item_list_table).insert(
            value['id'],
            value['name'],
            table_name
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{table_name} Itemname: {value['name']} ID: {value['id']} import complete")

    # SKILLGEM TABLE --------------------------------------------------
    table_name = 'SkillGem'
    response = (json.loads(index.send_request(item_types[table_name], index.current_league, table_name)))['lines']

    base_type = Table(table_name)
    db.execute(f'DELETE FROM {table_name}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(base_type).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['gemLevel'],
            value['gemQuality'],
            value['corrupted'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(item_list_table).insert(
            value['id'],
            value['name'],
            table_name
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{table_name} Itemname: {value['name']} ID: {value['id']} import complete")

    # UNIQUES TABLE --------------------------------------------------
    table_name = 'Uniques'
    base_type = Table(table_name)
    db.execute(f'DELETE FROM {table_name}')

    for uniqueType in unique_types.items():

        response = (json.loads(index.send_request(uniqueType[1], index.current_league, uniqueType[0])))['lines']

        for obj in response:
            value = map_values(obj)
            q = Query.into(base_type).insert(
                value['id'],
                value['name'],
                value['icon'],
                value['levelRequired'],
                value['baseType'],
                value['itemClass'],
                value['itemType'],
                value['chaosValue'],
                value['listingCount']
            )

            q_index = Query.into(item_list_table).insert(
                value['id'],
                value['name'],
                table_name
            )

            db.execute(str(q))
            db.execute(str(q_index))
            con.commit()
            print(f"{table_name} Itemname: {value['name']} ID: {value['id']} import complete")

    # ARTIFACT TABLE --------------------------------------------------
    table_name = 'Artifact'
    response = (json.loads(index.send_request(item_types[table_name], index.current_league, table_name)))['lines']

    base_type = Table(table_name)
    db.execute(f'DELETE FROM {table_name}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(base_type).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(item_list_table).insert(
            value['id'],
            value['name'],
            table_name
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{table_name} Itemname: {value['name']} ID: {value['id']} import complete")

    # DELIRIUM_ORB TABLE --------------------------------------------------
    table_name = 'DeliriumOrb'
    response = (json.loads(index.send_request(item_types[table_name], index.current_league, table_name)))['lines']

    base_type = Table(table_name)
    db.execute(f'DELETE FROM {table_name}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(base_type).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(item_list_table).insert(
            value['id'],
            value['name'],
            table_name
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{table_name} Itemname: {value['name']} ID: {value['id']} import complete")

    # INVITATION TABLE --------------------------------------------------
    table_name = 'Invitation'
    response = (json.loads(index.send_request(item_types[table_name], index.current_league, table_name)))['lines']

    base_type = Table(table_name)
    db.execute(f'DELETE FROM {table_name}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(base_type).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(item_list_table).insert(
            value['id'],
            value['name'],
            table_name
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{table_name} Itemname: {value['name']} ID: {value['id']} import complete")

    # MEMORY TABLE --------------------------------------------------
    table_name = 'Memory'
    response = (json.loads(index.send_request(item_types[table_name], index.current_league, table_name)))['lines']

    base_type = Table(table_name)
    db.execute(f'DELETE FROM {table_name}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(base_type).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(item_list_table).insert(
            value['id'],
            value['name'],
            table_name
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{table_name} Itemname: {value['name']} ID: {value['id']} import complete")


create_db_tables
refresh_db_values()