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
    "currencyitem",
    "uniqueitem",
    "gemitem",
    "rareitem",
    "magicitem",
    "whiteitem",
]

unique_types = {
    "UniqueMap": "itemoverview",
    "UniqueJewel": "itemoverview",
    "UniqueFlask": "itemoverview",
    "UniqueWeapon": "itemoverview",
    "UniqueArmour": "itemoverview",
    "UniqueAccessory": "itemoverview",
}

table_specs = [
    {
        "name": "BaseType",
        "fields": [
            {"name": "id", "type": "INTEGER"},
            {"name": "name", "type": ""},
            {"name": "icon", "type": ""},
            {"name": "levelRequired", "type": "INTEGER"},
            {"name": "baseType", "type": ""},
            {"name": "itemClass", "type": ""},
            {"name": "chaosValue", "type": "NUMERIC"},
            {"name": "listingCount", "type": "INTEGER"},
            {"name": "variant", "type": ""},
            {"name": "sparkline", "type": "NUMERIC"}
        ],
    },
    {
        "name": "Currency",
        "fields": [
            {"name": "name", "type": ""},
            {"name": "icon", "type": ""},
            {"name": "chaosEquivalent", "type": "NUMERIC"},
            {"name": "receiveSparkLine", "type": "NUMERIC"},
            {"name": "paySparkLine", "type": "NUMERIC"}
        ],
    },
    {
        "name": "DivinationCard",
        "fields": [
            {"name": "id", "type": "INTEGER"},
            {"name": "name", "type": ""},
            {"name": "icon", "type": ""},
            {"name": "chaosValue", "type": "NUMERIC"},
            {"name": "count", "type": "INTEGER"},
            {"name": "stackSize", "type": "INTEGER"},
            {"name": "listingCount", "type": "INTEGER"},
            {"name": "quality", "type": ""},
            {"name": "corrupted", "type": ""},
            {"name": "rewardType", "type": ""},
            {"name": "rewardAmount", "type": "INTEGER"},
            {"name": "reward", "type": ""},
            {"name": "sparkline", "type": "NUMERIC"}
        ],
    },
    {
        "name": "Essence",
        "fields": [
            {"name": "id", "type": "INTEGER"},
            {"name": "name", "type": ""},
            {"name": "icon", "type": ""},
            {"name": "chaosValue", "type": "NUMERIC"},
            {"name": "listingCount", "type": "INTEGER"},
            {"name": "mapTier", "type": "INTEGER"},
            {"name": "sparkline", "type": "NUMERIC"}
        ],
    },
    {
        "name": "Fossil",
        "fields": [
            {"name": "id", "type": "INTEGER"},
            {"name": "name", "type": ""},
            {"name": "icon", "type": ""},
            {"name": "chaosValue", "type": "NUMERIC"},
            {"name": "listingCount", "type": "INTEGER"},
            {"name": "sparkline", "type": "NUMERIC"}
        ],
    },
    {
        "name": "Fragment",
        "fields": [
            {"name": "name", "type": ""},
            {"name": "icon", "type": ""},
            {"name": "chaosEquivalent", "type": "NUMERIC"},
            {"name": "receiveSparkLine", "type": "NUMERIC"},
            {"name": "paySparkLine", "type": "NUMERIC"}
        ],
    },
    {
        "name": "Incubator",
        "fields": [
            {"name": "id", "type": "INTEGER"},
            {"name": "name", "type": ""},
            {"name": "icon", "type": ""},
            {"name": "chaosValue", "type": "NUMERIC"},
            {"name": "listingCount", "type": "INTEGER"},
            {"name": "sparkline", "type": "NUMERIC"}
        ],
    },
    {
        "name": "Oil",
        "fields": [
            {"name": "id", "type": "INTEGER"},
            {"name": "name", "type": ""},
            {"name": "icon", "type": ""},
            {"name": "chaosValue", "type": "NUMERIC"},
            {"name": "listingCount", "type": "INTEGER"},
            {"name": "sparkline", "type": "NUMERIC"}
        ],
    },
    {
        "name": "Resonator",
        "fields": [
            {"name": "id", "type": "INTEGER"},
            {"name": "name", "type": ""},
            {"name": "icon", "type": ""},
            {"name": "chaosValue", "type": "NUMERIC"},
            {"name": "listingCount", "type": "INTEGER"},
            {"name": "sparkline", "type": "NUMERIC"}
        ],
    },
    {
        "name": "Scarab",
        "fields": [
            {"name": "id", "type": "INTEGER"},
            {"name": "name", "type": ""},
            {"name": "icon", "type": ""},
            {"name": "chaosValue", "type": "NUMERIC"},
            {"name": "listingCount", "type": "INTEGER"},
            {"name": "sparkline", "type": "NUMERIC"}
        ],
    },
    {
        "name": "SkillGem",
        "fields": [
            {"name": "id", "type": "INTEGER"},
            {"name": "name", "type": ""},
            {"name": "icon", "type": ""},
            {"name": "chaosValue", "type": "NUMERIC"},
            {"name": "listingCount", "type": "INTEGER"},
            {"name": "gemLevel", "type": "INTEGER"},
            {"name": "quality", "type": "INTEGER"},
            {"name": "corrupted", "type": "INTEGER"},
            {"name": "sparkline", "type": "NUMERIC"}
        ],
    },
    {
        "name": "Uniques",
        "fields": [
            {"name": "id", "type": "INTEGER"},
            {"name": "name", "type": ""},
            {"name": "icon", "type": ""},
            {"name": "levelRequired", "type": "INTEGER"},
            {"name": "baseType", "type": ""},
            {"name": "itemClass", "type": ""},
            {"name": "itemType", "type": ""},
            {"name": "chaosValue", "type": "NUMERIC"},
            {"name": "listingCount", "type": "INTEGER"},
            {"name": "sparkline", "type": "NUMERIC"}
        ],
    },
    {
        "name": "Artifact",
        "fields": [
            {"name": "id", "type": "INTEGER"},
            {"name": "name", "type": ""},
            {"name": "icon", "type": ""},
            {"name": "chaosValue", "type": "NUMERIC"},
            {"name": "listingCount", "type": "INTEGER"},
            {"name": "sparkline", "type": "NUMERIC"}
        ],
    },
    {
        "name": "DeliriumOrb",
        "fields": [
            {"name": "id", "type": "INTEGER"},
            {"name": "name", "type": ""},
            {"name": "icon", "type": ""},
            {"name": "chaosValue", "type": "NUMERIC"},
            {"name": "listingCount", "type": "INTEGER"},
            {"name": "sparkline", "type": "NUMERIC"}
        ],
    },
    {
        "name": "Invitation",
        "fields": [
            {"name": "id", "type": "INTEGER"},
            {"name": "name", "type": ""},
            {"name": "icon", "type": ""},
            {"name": "chaosValue", "type": "NUMERIC"},
            {"name": "listingCount", "type": "INTEGER"},
            {"name": "sparkline", "type": "NUMERIC"}
        ],
    },
    {
        "name": "Memory",
        "fields": [
            {"name": "id", "type": "INTEGER"},
            {"name": "name", "type": ""},
            {"name": "icon", "type": ""},
            {"name": "chaosValue", "type": "NUMERIC"},
            {"name": "listingCount", "type": "INTEGER"},
            {"name": "sparkline", "type": "NUMERIC"}
        ],
    },
    {
        "name": "ItemList",
        "fields": [
            {"name": "id", "type": "INTEGER"},
            {"name": "name", "type": "TEXT"},
            {"name": "table_name", "type": "TEXT"},
        ],
    },
]
