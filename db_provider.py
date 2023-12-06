import json
import sqlite3
from pypika import Query, Table, Field
import re

import index
import poe_types

con = sqlite3.connect("poeflipper.db")
db = con.cursor()
ItemList = 'ItemList'

itemTypes = poe_types.itemTypes
reward_types = poe_types.rewardTypes
uniqueTypes = poe_types.uniqueTypes


def create_db_tables():
    db.execute(
        "CREATE TABLE IF NOT EXISTS BaseType(id INTEGER, name, icon, levelRequired INTEGER, baseType, itemClass, chaosValue NUMERIC, listingCount, variant)")
    db.execute("CREATE TABLE IF NOT EXISTS Currency(name, icon, chaosEquivalent NUMERIC)")
    db.execute(
        "CREATE TABLE IF NOT EXISTS DivinationCard(id INTEGER, name, icon, stackSize INTEGER, reward, rewardAmount INTEGER, rewardType, chaosValue NUMERIC, count INTEGER, listingCount INTEGER)")
    db.execute(
        "CREATE TABLE IF NOT EXISTS Essence(id INTEGER, name, icon, mapTier INTEGER, chaosValue NUMERIC, listingCount INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS Fossil(id INTEGER, name, icon, chaosValue NUMERIC, listingCount INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS Fragment(name, icon, chaosEquivalent NUMERIC)")
    db.execute("CREATE TABLE IF NOT EXISTS Incubator(id INTEGER, name, icon, chaosValue NUMERIC, listingCount INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS Oil(id INTEGER, name, icon, chaosValue NUMERIC, listingCount INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS Resonator(id INTEGER, name, icon, chaosValue NUMERIC, listingCount INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS Scarab(id INTEGER, name, icon, chaosValue NUMERIC, listingCount INTEGER)")
    db.execute(
        "CREATE TABLE IF NOT EXISTS SkillGem(id INTEGER, name, icon, gemLevel INTEGER, gemQuality INTEGER, corrupted INTEGER, chaosValue NUMERIC, listingCount INTEGER)")
    db.execute(
        "CREATE TABLE IF NOT EXISTS Uniques(id INTEGER, name, icon, levelRequired INTEGER, baseType, itemClass, itemType, chaosValue NUMERIC, listingCount INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS Artifact(id INTEGER, name, icon, chaosValue NUMERIC, listingCount INTEGER)")
    db.execute(
        "CREATE TABLE IF NOT EXISTS DeliriumOrb(id INTEGER, name, icon, chaosValue NUMERIC, listingCount INTEGER)")
    db.execute(
        "CREATE TABLE IF NOT EXISTS Invitation(id INTEGER, name, icon, chaosValue NUMERIC, listingCount INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS Memory(id INTEGER, name, icon, chaosValue NUMERIC, listingCount INTEGER)")

    db.execute("CREATE TABLE IF NOT EXISTS ItemList(id INTEGER, name TEXT, table_name TEXT)")

    # https://pypika.readthedocs.io/en/latest/2_tutorial.html
    from pypika import Query, Table, Field

    # https://docs.python.org/3/library/sqlite3.html
    # q = Query.from_('movie').select('name', 'year', 'score')
    #
    # con = sqlite3.connect("tutorial.db")
    # cur = con.cursor()
    # res = cur.execute(str(q))
    #
    # print(res.fetchall())


def map_values(obj, type=''):
    values = {}

    if 'id' in obj:
        values['id'] = obj['id']
    if 'name' in obj:
        values['name'] = obj['name']
    if 'currencyTypeName' in obj:
        values['name'] = obj['currencyTypeName']
    if 'icon' in obj:
        values['icon'] = obj['icon']
    else:
        values['icon'] = ''
    if 'levelRequired' in obj:
        values['levelRequired'] = obj['levelRequired']
    else:
        values['levelRequired'] = 0
    if 'baseType' in obj:
        values['baseType'] = obj['baseType']
    if 'itemClass' in obj:
        values['itemClass'] = obj['itemClass']
    if 'itemType' in obj:
        values['itemType'] = obj['itemType']
    else:
        values['itemType'] = ''
    if 'chaosValue' in obj:
        values['chaosValue'] = obj['chaosValue']
    if 'chaosEquivalent' in obj:
        values['chaosValue'] = obj['chaosEquivalent']
    if 'listingCount' in obj:
        values['listingCount'] = obj['listingCount']
    if 'stackSize' in obj:
        values['stackSize'] = obj['stackSize']
    else:
        values['stackSize'] = 1
    if 'count' in obj:
        values['count'] = obj['count']
    if 'mapTier' in obj:
        values['mapTier'] = obj['mapTier']
    else:
        values['mapTier'] = 1
    if 'gemLevel' in obj:
        values['gemLevel'] = obj['gemLevel']
    if 'gemQuality' in obj:
        values['gemQuality'] = obj['gemQuality']
    else:
        values['gemQuality'] = 0
    if 'corrupted' in obj:
        values['corrupted'] = 1
    else:
        values['corrupted'] = 0
    if 'variant' in obj:
        values['variant'] = obj['variant']
    else:
        values['variant'] = ''

    if type == 'DivinationCard':
        # Divination Card reward regex
        pattern = r'<(currencyitem|uniqueitem|gemitem|rareitem|magicitem|whiteitem|divination)+>\s*{(?:(\d+)x\s*)?([^}]+)}'

        for explicitModifier in obj['explicitModifiers']:
            match = re.search(pattern, explicitModifier['text'])

            if match:
                values['rewardType'] = match.group(1)
                values['rewardAmount'] = match.group(2) or 1
                values['reward'] = match.group(3)
            else:
                values['rewardType'] = ''
                values['rewardAmount'] = '1'
                values['reward'] = ''

    return values


def refresh_db_values():
    db.execute(f'DELETE FROM {ItemList}')
    itemListTable = Table(ItemList)

    # BASETYPE TABLE --------------------------------------------------
    tableName = 'BaseType'
    response = (json.loads(index.send_request(itemTypes[tableName], index.currentLeague, tableName)))['lines']

    BaseType = Table(tableName)
    db.execute(f'DELETE FROM {tableName}')

    for obj in response:
        value = map_values(obj)

        q = Query.into(BaseType).insert(
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

        q_index = Query.into(itemListTable).insert(
            value['id'],
            value['name'],
            tableName
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{tableName} Itemname: {value['name']} ID: {value['id']} import complete")

    # CURRENCY TABLE --------------------------------------------------
    tableName = 'Currency'
    response = (json.loads(index.send_request(itemTypes[tableName], index.currentLeague, tableName)))['lines']

    BaseType = Table(tableName)
    db.execute(f'DELETE FROM {tableName}')

    for obj in response:
        value = map_values(obj)

        q = Query.into(BaseType).insert(
            value['name'],
            value['icon'],
            value['chaosValue'],
        )

        q_index = Query.into(itemListTable).insert(
            '',
            value['name'],
            tableName
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{tableName} Itemname: {value['name']} import complete")

    # DIVINATIONCARD TABLE --------------------------------------------------
    tableName = 'DivinationCard'
    response = (json.loads(index.send_request(itemTypes[tableName], index.currentLeague, tableName)))['lines']

    BaseType = Table(tableName)
    db.execute(f'DELETE FROM {tableName}')

    for obj in response:
        value = map_values(obj, 'DivinationCard')

        q = Query.into(BaseType).insert(
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

        q_index = Query.into(itemListTable).insert(
            value['id'],
            value['name'],
            tableName
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{tableName} Itemname: {value['name']} ID: {value['id']} import complete")

    # ESSENCE TABLE --------------------------------------------------
    tableName = 'Essence'
    response = (json.loads(index.send_request(itemTypes[tableName], index.currentLeague, tableName)))['lines']

    BaseType = Table(tableName)
    db.execute(f'DELETE FROM {tableName}')

    for obj in response:
        value = map_values(obj)

        q = Query.into(BaseType).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['mapTier'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(itemListTable).insert(
            value['id'],
            value['name'],
            tableName
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{tableName} Itemname: {value['name']} ID: {value['id']} import complete")

    # FOSSIL TABLE --------------------------------------------------
    tableName = 'Fossil'
    response = (json.loads(index.send_request(itemTypes[tableName], index.currentLeague, tableName)))['lines']

    BaseType = Table(tableName)
    db.execute(f'DELETE FROM {tableName}')

    for obj in response:
        value = map_values(obj)

        q = Query.into(BaseType).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(itemListTable).insert(
            value['id'],
            value['name'],
            tableName
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{tableName} Itemname: {value['name']} ID: {value['id']} import complete")

    # FRAGMENT TABLE --------------------------------------------------
    tableName = 'Fragment'
    response = (json.loads(index.send_request(itemTypes[tableName], index.currentLeague, tableName)))['lines']

    BaseType = Table(tableName)
    db.execute(f'DELETE FROM {tableName}')

    for obj in response:
        value = map_values(obj)

        q = Query.into(BaseType).insert(
            value['name'],
            value['icon'],
            value['chaosValue'],
        )

        q_index = Query.into(itemListTable).insert(
            '',
            value['name'],
            tableName
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{tableName} Itemname: {value['name']} import complete")

    # INCUBATOR TABLE --------------------------------------------------
    tableName = 'Incubator'
    response = (json.loads(index.send_request(itemTypes[tableName], index.currentLeague, tableName)))['lines']

    BaseType = Table(tableName)
    db.execute(f'DELETE FROM {tableName}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(BaseType).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(itemListTable).insert(
            value['id'],
            value['name'],
            tableName
        )

        db.execute(str(q))
        db.execute(str(q_index))

        con.commit()
        print(f"{tableName} Itemname: {value['name']} ID: {value['id']} import complete")

    # OIL TABLE --------------------------------------------------
    tableName = 'Oil'
    response = (json.loads(index.send_request(itemTypes[tableName], index.currentLeague, tableName)))['lines']

    BaseType = Table(tableName)
    db.execute(f'DELETE FROM {tableName}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(BaseType).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(itemListTable).insert(
            value['id'],
            value['name'],
            tableName
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{tableName} Itemname: {value['name']} ID: {value['id']} import complete")

    # RESONATOR TABLE --------------------------------------------------
    tableName = 'Resonator'
    response = (json.loads(index.send_request(itemTypes[tableName], index.currentLeague, tableName)))['lines']

    BaseType = Table(tableName)
    db.execute(f'DELETE FROM {tableName}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(BaseType).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(itemListTable).insert(
            value['id'],
            value['name'],
            tableName
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{tableName} Itemname: {value['name']} ID: {value['id']} import complete")

    # SCARAB TABLE --------------------------------------------------
    tableName = 'Scarab'
    response = (json.loads(index.send_request(itemTypes[tableName], index.currentLeague, tableName)))['lines']

    BaseType = Table(tableName)
    db.execute(f'DELETE FROM {tableName}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(BaseType).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(itemListTable).insert(
            value['id'],
            value['name'],
            tableName
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{tableName} Itemname: {value['name']} ID: {value['id']} import complete")

    # SKILLGEM TABLE --------------------------------------------------
    tableName = 'SkillGem'
    response = (json.loads(index.send_request(itemTypes[tableName], index.currentLeague, tableName)))['lines']

    BaseType = Table(tableName)
    db.execute(f'DELETE FROM {tableName}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(BaseType).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['gemLevel'],
            value['gemQuality'],
            value['corrupted'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(itemListTable).insert(
            value['id'],
            value['name'],
            tableName
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{tableName} Itemname: {value['name']} ID: {value['id']} import complete")

    # UNIQUES TABLE --------------------------------------------------
    tableName = 'Uniques'
    BaseType = Table(tableName)
    db.execute(f'DELETE FROM {tableName}')

    for uniqueType in uniqueTypes.items():

        response = (json.loads(index.send_request(uniqueType[1], index.currentLeague, uniqueType[0])))['lines']

        for obj in response:
            value = map_values(obj)
            q = Query.into(BaseType).insert(
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

            q_index = Query.into(itemListTable).insert(
                value['id'],
                value['name'],
                tableName
            )

            db.execute(str(q))
            db.execute(str(q_index))
            con.commit()
            print(f"{tableName} Itemname: {value['name']} ID: {value['id']} import complete")

    # ARTIFACT TABLE --------------------------------------------------
    tableName = 'Artifact'
    response = (json.loads(index.send_request(itemTypes[tableName], index.currentLeague, tableName)))['lines']

    BaseType = Table(tableName)
    db.execute(f'DELETE FROM {tableName}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(BaseType).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(itemListTable).insert(
            value['id'],
            value['name'],
            tableName
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{tableName} Itemname: {value['name']} ID: {value['id']} import complete")

    # DELIRIUM_ORB TABLE --------------------------------------------------
    tableName = 'DeliriumOrb'
    response = (json.loads(index.send_request(itemTypes[tableName], index.currentLeague, tableName)))['lines']

    BaseType = Table(tableName)
    db.execute(f'DELETE FROM {tableName}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(BaseType).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(itemListTable).insert(
            value['id'],
            value['name'],
            tableName
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{tableName} Itemname: {value['name']} ID: {value['id']} import complete")

    # INVITATION TABLE --------------------------------------------------
    tableName = 'Invitation'
    response = (json.loads(index.send_request(itemTypes[tableName], index.currentLeague, tableName)))['lines']

    BaseType = Table(tableName)
    db.execute(f'DELETE FROM {tableName}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(BaseType).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(itemListTable).insert(
            value['id'],
            value['name'],
            tableName
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{tableName} Itemname: {value['name']} ID: {value['id']} import complete")

    # MEMORY TABLE --------------------------------------------------
    tableName = 'Memory'
    response = (json.loads(index.send_request(itemTypes[tableName], index.currentLeague, tableName)))['lines']

    BaseType = Table(tableName)
    db.execute(f'DELETE FROM {tableName}')

    for obj in response:
        value = map_values(obj)
        q = Query.into(BaseType).insert(
            value['id'],
            value['name'],
            value['icon'],
            value['chaosValue'],
            value['listingCount']
        )

        q_index = Query.into(itemListTable).insert(
            value['id'],
            value['name'],
            tableName
        )

        db.execute(str(q))
        db.execute(str(q_index))
        con.commit()
        print(f"{tableName} Itemname: {value['name']} ID: {value['id']} import complete")


create_db_tables
refresh_db_values