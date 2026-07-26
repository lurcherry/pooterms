import random

from utils.items import get_item




RARITY_CHANCE = {

    "⚪ Common": 95,

    "🟢 Uncommon": 50,

    "🔵 Rare": 15,

    "🟣 Epic": 5,

    "🟡 Legendary": 1,

    "🌈 Divine": 0.1
}




def roll_drop(
    possible_items
):


    drops = []



    for item_name in possible_items:


        item = get_item(
            item_name
        )


        if item is None:

            continue



        rarity = item.get(
            "rarity",
            "⚪ Common"
        )



        chance = RARITY_CHANCE.get(

            rarity,

            50

        )



        roll = random.uniform(
            0,
            100
        )



        if roll <= chance:


            amount = random.randint(
                1,
                3
            )


            drops.append(

                {

                    "item": item_name,

                    "amount": amount,

                    "rarity": rarity

                }

            )



    return drops


def format_loot(
    drops
):


    if not drops:

        return "Nothing dropped..."



    text = ""



    for drop in drops:


        item = get_item(
            drop["item"]
        )


        if item:


            text += (

                f"{item['emoji']} "

                f"**{drop['item']}** ×{drop['amount']}\n"

                f"{drop['rarity']}\n\n"

            )


        else:


            text += (

                f"📦 **{drop['item']}** "
                f"×{drop['amount']}\n\n"

            )



    return text




def get_drop_message(
    drops,
    name
):


    messages = []



    for drop in drops:


        rarity = drop.get(
            "rarity"
        )


        item = drop.get(
            "item"
        )



        if rarity == "🟣 Epic":


            messages.append(

                f"✨ **{name}**, you found "
                f"**{item}**!"

            )



        elif rarity == "🟡 Legendary":


            messages.append(

                f"🌟 **{name}**, NO WAY!\n"

                f"You obtained **{item}**!"

            )



        elif rarity == "🌈 Divine":


            messages.append(

                f"🌈 **{name}**, THE STARS HAVE ALIGNED!\n"

                f"You obtained **{item}**!"

            )



    return "\n\n".join(
        messages
    )

from utils.items import ITEMS, LOOTBOX_POOL


def roll_lootbox(lootbox_name):

    if lootbox_name not in LOOTBOX_POOL:
        return None

    pool = LOOTBOX_POOL[lootbox_name]

    rarity = random.choices(
        list(pool.keys()),
        weights=list(pool.values()),
        k=1
    )[0]

    possible_items = []

    for item_name, item in ITEMS.items():

        if item["type"] == "lootbox":
            continue

        if item["rarity"] == rarity:
            possible_items.append(item_name)

    if not possible_items:
        return None

    return random.choice(possible_items)