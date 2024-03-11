# This file is a document for all item types that poe currently offers and which we want to
# check

GREEN = "\033[92m"
RESET = "\033[0m"
BLUE = "\033[94m"

item_types = {
    "Currency": "currencyoverview",
    "Fragment": "currencyoverview",
    "Oil": "itemoverview",
    "Incubator": "itemoverview",
    "Scarab": "itemoverview",
    "Fossil": "itemoverview",
    "Resonator": "itemoverview",
    "Essence": "itemoverview",
    "DivinationCard": "itemoverview",
    "SkillGem": "itemoverview",
    "BaseType": "itemoverview",
    "Artifact": "itemoverview",
    "DeliriumOrb": "itemoverview",
    "Invitation": "itemoverview",
    "Memory": "itemoverview",
}

reward_types = [
    'currencyitem',
    'uniqueitem',
    'gemitem',
    'rareitem',
    'magicitem',
    'whiteitem'
]

unique_types = {
    "UniqueMap": "itemoverview",
    "UniqueJewel": "itemoverview",
    "UniqueFlask": "itemoverview",
    "UniqueWeapon": "itemoverview",
    "UniqueArmour": "itemoverview",
    "UniqueAccessory": "itemoverview"
}

table_specs = [
    {
        'name': 'BaseType',
        'fields': [
            {'name': 'id', 'type': 'INTEGER'},
            {'name': 'name', 'type': ''},
            {'name': 'icon', 'type': ''},
            {'name': 'levelRequired', 'type': 'INTEGER'},
            {'name': 'baseType', 'type': ''},
            {'name': 'itemClass', 'type': ''},
            {'name': 'chaosValue', 'type': 'NUMERIC'},
            {'name': 'listingCount', 'type': 'INTEGER'},
            {'name': 'variant', 'type': ''},
        ],
    },
    {
        'name': 'Currency',
        'fields': [
            {'name': 'name', 'type': ''},
            {'name': 'icon', 'type': ''},
            {'name': 'chaosEquivalent', 'type': 'NUMERIC'},
        ],
    },
    {
        'name': 'DivinationCard',
        'fields': [
            {'name': 'id', 'type': 'INTEGER'},
            {'name': 'name', 'type': ''},
            {'name': 'icon', 'type': ''},
            {'name': 'chaosValue', 'type': 'NUMERIC'},
            {'name': 'count', 'type': 'INTEGER'},
            {'name': 'stackSize', 'type': 'INTEGER'},
            {'name': 'listingCount', 'type': 'INTEGER'},
            {'name': 'quality', 'type': ''},
            {'name': 'corrupted', 'type': ''},
            {'name': 'rewardType', 'type': ''},
            {'name': 'rewardAmount', 'type': 'INTEGER'},
            {'name': 'reward', 'type': ''},
        ],
    },
    {
        'name': 'Essence',
        'fields': [
            {'name': 'id', 'type': 'INTEGER'},
            {'name': 'name', 'type': ''},
            {'name': 'icon', 'type': ''},
            {'name': 'chaosValue', 'type': 'NUMERIC'},
            {'name': 'listingCount', 'type': 'INTEGER'},
            {'name': 'mapTier', 'type': 'INTEGER'},
        ],
    },
    {
        'name': 'Fossil',
        'fields': [
            {'name': 'id', 'type': 'INTEGER'},
            {'name': 'name', 'type': ''},
            {'name': 'icon', 'type': ''},
            {'name': 'chaosValue', 'type': 'NUMERIC'},
            {'name': 'listingCount', 'type': 'INTEGER'},
        ],
    },
    {
        'name': 'Fragment',
        'fields': [
            {'name': 'name', 'type': ''},
            {'name': 'icon', 'type': ''},
            {'name': 'chaosEquivalent', 'type': 'NUMERIC'},
        ],
    },
    {
        'name': 'Incubator',
        'fields': [
            {'name': 'id', 'type': 'INTEGER'},
            {'name': 'name', 'type': ''},
            {'name': 'icon', 'type': ''},
            {'name': 'chaosValue', 'type': 'NUMERIC'},
            {'name': 'listingCount', 'type': 'INTEGER'},
        ],
    },
    {
        'name': 'Oil',
        'fields': [
            {'name': 'id', 'type': 'INTEGER'},
            {'name': 'name', 'type': ''},
            {'name': 'icon', 'type': ''},
            {'name': 'chaosValue', 'type': 'NUMERIC'},
            {'name': 'listingCount', 'type': 'INTEGER'},
        ],
    },
    {
        'name': 'Resonator',
        'fields': [
            {'name': 'id', 'type': 'INTEGER'},
            {'name': 'name', 'type': ''},
            {'name': 'icon', 'type': ''},
            {'name': 'chaosValue', 'type': 'NUMERIC'},
            {'name': 'listingCount', 'type': 'INTEGER'},
        ],
    },
    {
        'name': 'Scarab',
        'fields': [
            {'name': 'id', 'type': 'INTEGER'},
            {'name': 'name', 'type': ''},
            {'name': 'icon', 'type': ''},
            {'name': 'chaosValue', 'type': 'NUMERIC'},
            {'name': 'listingCount', 'type': 'INTEGER'},
        ],
    },
    {
        'name': 'SkillGem',
        'fields': [
            {'name': 'id', 'type': 'INTEGER'},
            {'name': 'name', 'type': ''},
            {'name': 'icon', 'type': ''},
            {'name': 'chaosValue', 'type': 'NUMERIC'},
            {'name': 'listingCount', 'type': 'INTEGER'},
            {'name': 'gemLevel', 'type': 'INTEGER'},
            {'name': 'quality', 'type': 'INTEGER'},
            {'name': 'corrupted', 'type': 'INTEGER'},
        ],
    },
    {
        'name': 'Uniques',
        'fields': [
            {'name': 'id', 'type': 'INTEGER'},
            {'name': 'name', 'type': ''},
            {'name': 'icon', 'type': ''},
            {'name': 'levelRequired', 'type': 'INTEGER'},
            {'name': 'baseType', 'type': ''},
            {'name': 'itemClass', 'type': ''},
            {'name': 'itemType', 'type': ''},
            {'name': 'chaosValue', 'type': 'NUMERIC'},
            {'name': 'listingCount', 'type': 'INTEGER'},
        ],
    },
    {
        'name': 'Artifact',
        'fields': [
            {'name': 'id', 'type': 'INTEGER'},
            {'name': 'name', 'type': ''},
            {'name': 'icon', 'type': ''},
            {'name': 'chaosValue', 'type': 'NUMERIC'},
            {'name': 'listingCount', 'type': 'INTEGER'},
        ],
    },
    {
        'name': 'DeliriumOrb',
        'fields': [
            {'name': 'id', 'type': 'INTEGER'},
            {'name': 'name', 'type': ''},
            {'name': 'icon', 'type': ''},
            {'name': 'chaosValue', 'type': 'NUMERIC'},
            {'name': 'listingCount', 'type': 'INTEGER'},
        ],
    },
    {
        'name': 'Invitation',
        'fields': [
            {'name': 'id', 'type': 'INTEGER'},
            {'name': 'name', 'type': ''},
            {'name': 'icon', 'type': ''},
            {'name': 'chaosValue', 'type': 'NUMERIC'},
            {'name': 'listingCount', 'type': 'INTEGER'},
        ],
    },
    {
        'name': 'Memory',
        'fields': [
            {'name': 'id', 'type': 'INTEGER'},
            {'name': 'name', 'type': ''},
            {'name': 'icon', 'type': ''},
            {'name': 'chaosValue', 'type': 'NUMERIC'},
            {'name': 'listingCount', 'type': 'INTEGER'},
        ],
    },
    {
        'name': 'ItemList',
        'fields': [
            {'name': 'id', 'type': 'INTEGER'},
            {'name': 'name', 'type': 'TEXT'},
            {'name': 'table_name', 'type': 'TEXT'},
        ],
    },
]