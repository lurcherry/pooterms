ITEMS = {




    "Wooden Axe": {

        "emoji": "🪓",

        "type": "weapon",

        "rarity": "⚪ Common",

        "price": 50,

        "sell": 25,

        "attack": 5,

        "defense": 0,

        "durability": 50

    },


    "Iron Sword": {

        "emoji": "⚔️",

        "type": "weapon",

        "rarity": "🟢 Uncommon",

        "price": 500,

        "sell": 250,

        "attack": 10,

        "defense": 0,

        "durability": 120

    },


    "Magic Staff": {

        "emoji": "🪄",

        "type": "weapon",

        "rarity": "🔵 Rare",

        "price": 1500,

        "sell": 750,

        "attack": 18,

        "defense": 0,

        "durability": 150

    },


    "Shadow Dagger": {

        "emoji": "🗡️",

        "type": "weapon",

        "rarity": "🟣 Epic",

        "price": 5000,

        "sell": 2500,

        "attack": 30,

        "defense": 0,

        "durability": 200

    },


    "Phoenix Greatsword": {

        "emoji": "🔥",

        "type": "weapon",

        "rarity": "🟡 Legendary",

        "price": 15000,

        "sell": 7500,

        "attack": 50,

        "defense": 0,

        "durability": 300

    },


    "Void Reaver": {

        "emoji": "🌌",

        "type": "weapon",

        "rarity": "🌈 Divine",

        "price": 50000,

        "sell": 25000,

        "attack": 80,

        "defense": 0,

        "durability": 500

    },



    "Leather Armor": {

        "emoji": "🥋",

        "type": "armor",

        "rarity": "⚪ Common",

        "price": 100,

        "sell": 50,

        "attack": 0,

        "defense": 5,

        "durability": 80

    },


    "Iron Armor": {

        "emoji": "🛡️",

        "type": "armor",

        "rarity": "🟢 Uncommon",

        "price": 800,

        "sell": 400,

        "attack": 0,

        "defense": 12,

        "durability": 150

    },


    "Knight Armor": {

        "emoji": "⚔️",

        "type": "armor",

        "rarity": "🔵 Rare",

        "price": 2500,

        "sell": 1250,

        "attack": 0,

        "defense": 20,

        "durability": 200

    },


    "Guardian Mail": {

        "emoji": "🛡️",

        "type": "armor",

        "rarity": "🟣 Epic",

        "price": 7000,

        "sell": 3500,

        "attack": 0,

        "defense": 35,

        "durability": 280

    },


    "Dragon Plate": {

        "emoji": "🐉",

        "type": "armor",

        "rarity": "🟡 Legendary",

        "price": 20000,

        "sell": 10000,

        "attack": 0,

        "defense": 55,

        "durability": 400

    },


    "Celestial Aegis": {

        "emoji": "🌈",

        "type": "armor",

        "rarity": "🌈 Divine",

        "price": 60000,

        "sell": 30000,

        "attack": 0,

        "defense": 90,

        "durability": 600

    },
    
    "Small Health Potion": {
        "emoji": "❤️",
        
        "type": "potion",
        
        "rarity": "⚪ Common",
        
        "price": 75,
        
        "sell": 35,
        
        "heal": 25
        
    },
    
    
    "Greater Health Potion": {
        
        "emoji": "💚",
        
        "type": "potion",
        
        "rarity": "🟢 Uncommon",
        
        "price": 250,
        
        "sell": 125,
        
        "heal": 50

    },
    
    
    "Supreme Health Potion": {
        
        "emoji": "💙",
        
        "type": "potion",
        
        "rarity": "🔵 Rare",
        
        "price": 750,
        
        "sell": 375,
        
        "heal": 100
        
    },
    
    "Lucky Lootbox": {
        
        "emoji": "🍀",
        
        "type": "lootbox",
        
        "rarity": "⚪ Common",
        
        "price": 500,
        
        "sell": 250
        
    },
    
    
    "Fortune Lootbox": {
        
        "emoji": "🌟",
        
        "type": "lootbox",
        
        "rarity": "🔵 Rare",
        
        "price": 2000,
        
        "sell": 1000
        
    },
    
    
    "Mythic Lootbox": {
        
        "emoji": "💎",
        
        "type": "lootbox",
        
        "rarity": "🟣 Epic",
        
        "price": 8000,
        
        "sell": 4000
        
    },
    
    
    "Divine Lootbox": {
        
        
        "emoji": "👑",
        
        "type": "lootbox",
        
        "rarity": "🌈 Divine",
        
        "price": 30000,
        
        "sell": 15000
        
    },


    "Slime Gel": {
        
        "emoji": "🟢",
        
        "type": "material",
        
        "rarity": "⚪ Common",
        
        "price": 20,

        "sell": 10

    },


    "Wolf Fur": {

        "emoji": "🐺",

        "type": "material",

        "rarity": "🟢 Uncommon",

        "price": 80,

        "sell": 40

    },


    "Goblin Ear": {

        "emoji": "👂",

        "type": "material",

        "rarity": "🔵 Rare",

        "price": 250,

        "sell": 125

    },


    "Dragon Scale": {

        "emoji": "🐉",

        "type": "material",

        "rarity": "🟡 Legendary",

        "price": 5000,

        "sell": 2500

    }


}



def get_item(name):

    for item_name, item in ITEMS.items():

        if item_name.lower() == name.lower():

            return item

    return None


def is_weapon(
    name
):

    item = get_item(
        name
    )

    if item:

        return item.get(
            "type"
        ) == "weapon"

    return False



def is_armor(
    name
):

    item = get_item(
        name
    )

    if item:

        return item.get(
            "type"
        ) == "armor"

    return False



def is_potion(
    name
):

    item = get_item(
        name
    )

    if item:

        return item.get(
            "type"
        ) == "potion"

    return False



def get_emoji(
    name
):

    item = get_item(
        name
    )

    if item:

        return item.get(
            "emoji",
            "📦"
        )

    return "📦"



def get_rarity(
    name
):

    item = get_item(
        name
    )

    if item:

        return item.get(
            "rarity",
            "⚪ Common"
        )

    return "⚪ Common"



def sell_price(
    name
):

    item = get_item(
        name
    )

    if item:

        return item.get(
            "sell",
            0
        )

    return 0


def is_material(name):
    item = ITEMS.get(name)

    if not item:
        return False

    return item.get("type") == "material"

SHOP_CHANCE = {

    "⚪ Common": 100,

    "🟢 Uncommon": 100,

    "🔵 Rare": 60,

    "🟣 Epic": 30,

    "🟡 Legendary": 8,

    "🌈 Divine": 2

}


SHOP_STOCK = {

    "⚪ Common": (10, 25),

    "🟢 Uncommon": (6, 15),

    "🔵 Rare": (3, 8),

    "🟣 Epic": (1, 3),

    "🟡 Legendary": (1, 1),

    "🌈 Divine": (1, 1)

}


LOOTBOX_POOL = {

    "Lucky Lootbox": {

        "⚪ Common": 80,

        "🟢 Uncommon": 20

    },

    "Fortune Lootbox": {

        "🟢 Uncommon": 75,

        "🔵 Rare": 25

    },

    "Mythic Lootbox": {

        "🔵 Rare": 70,

        "🟣 Epic": 30

    },

    "Divine Lootbox": {

        "🟣 Epic": 75,

        "🟡 Legendary": 22,

        "🌈 Divine": 3

    }

}