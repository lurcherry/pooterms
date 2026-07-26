import discord
import aiosqlite

from discord.ext import commands

from utils.colors import Colors
from utils.items import (
    ITEMS,
    get_item,
    is_weapon,
    is_armor
)

DB_PATH = "data/database.db"


class Equipment(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def equip(
        self,
        ctx,
        *,
        item_name
    ):

        user_id = ctx.author.id
        name = ctx.author.display_name

        original_name = item_name

        item = get_item(item_name)

        if item is None:

            await ctx.send(
                f"🧰 ┃ **{name}**, that item does not exist."
            )

            return
        
        item_name = next(
            key for key, value in ITEMS.items()
            if value == item
        )

        if not is_weapon(item_name) and not is_armor(item_name):

            await ctx.send(
                f"⚔️ ┃ **{name}**, you can only equip weapons or armor."
            )

            return

        async with aiosqlite.connect(DB_PATH) as db:

            cursor = await db.execute(
                """
                SELECT amount
                FROM inventory
                WHERE user_id = ?
                AND item_name = ?
                """,
                (
                    user_id,
                    item_name
                )
            )

            owned = await cursor.fetchone()

        if owned is None:

            await ctx.send(
                f"⚔️ ┃ **{name}**, you cannot equip something you don’t own.\n"
                "Monsters are not going to drop themselves. Try `poo fight`."
            )

            return

        async with aiosqlite.connect(DB_PATH) as db:

            cursor = await db.execute(
                """
                SELECT weapon,
                       armor
                FROM equipment
                WHERE user_id = ?
                """,
                (user_id,)
            )

            current = await cursor.fetchone()

            if current is None:

                await db.execute(
                    """
                    INSERT INTO equipment(user_id)
                    VALUES(?)
                    """,
                    (user_id,)
                )

                await db.commit()

                current = (
                    None,
                    None
                )

        if is_weapon(item_name):

            if current[0] == item_name:

                await ctx.send(
                    f"🛡️ ┃ **{name}**, you’re already holding that weapon!\n"
                    "One sword is enough... unless you grow another arm."
                )

                return

            async with aiosqlite.connect(DB_PATH) as db:

                await db.execute(
                    """
                    UPDATE equipment
                    SET weapon = ?,
                        weapon_durability = ?
                    WHERE user_id = ?
                    """,
                    (
                        item_name,
                        item["durability"],
                        user_id
                    )
                )

                await db.commit()

            embed = discord.Embed(
                title="⚔️ ┃ Item Equipped!",
                description=(
                    f"**{name}** equipped\n\n"
                    f"{item['emoji']} **{item_name}**\n"
                    f"{item['rarity']}\n\n"
                    f"⚔️ ┃ Attack : **+{item['attack']}**\n"
                    f"🔨 ┃ Durability : **{item['durability']}/{item['durability']}**"
                ),
                color=Colors.SUCCESS
            )

            await ctx.send(embed=embed)

            return

        if is_armor(item_name):

            if current[1] == item_name:

                await ctx.send(
                    f"🛡️ ┃ **{name}**, you’re already wearing that armor!"
                )

                return

            async with aiosqlite.connect(DB_PATH) as db:

                await db.execute(
                    """
                    UPDATE equipment
                    SET armor = ?,
                        armor_durability = ?
                    WHERE user_id = ?
                    """,
                    (
                        item_name,
                        item["durability"],
                        user_id
                    )
                )

                await db.commit()

            embed = discord.Embed(
                title="⚔️ ┃ Item Equipped!",
                description=(
                    f"**{name}** equipped\n\n"
                    f"{item['emoji']} **{item_name}**\n"
                    f"{item['rarity']}\n\n"
                    f"🛡️ ┃ Defense : **+{item['defense']}**\n"
                    f"🔨 ┃ Durability : **{item['durability']}/{item['durability']}**"
                ),
                color=Colors.SUCCESS
            )

            await ctx.send(embed=embed)

    @commands.command()
    async def unequip(
        self,
        ctx,
        *,
        item_name
    ):

        user_id = ctx.author.id
        name = ctx.author.display_name

        item = get_item(item_name)

        if item is None:
            await ctx.send(
                f"🧰 ┃ **{name}**, that item does not exist."
            )
            return

        canonical_name = next(
            key for key, value in ITEMS.items()
            if value == item
        )

        async with aiosqlite.connect(DB_PATH) as db:

            cursor = await db.execute(
                """
                SELECT weapon,
                       armor
                FROM equipment
                WHERE user_id = ?
                """,
                (user_id,)
            )

            equipment = await cursor.fetchone()

        if equipment is None:

            await ctx.send(
                f"⚔️ ┃ **{name}**, you have nothing equipped."
            )

            return

        removed = False

        async with aiosqlite.connect(DB_PATH) as db:


            if equipment[0] and equipment[0].lower() == canonical_name.lower():

                await db.execute(
                    """
                    UPDATE equipment
                    SET weapon = NULL,
                        weapon_durability = 0
                    WHERE user_id = ?
                    """,
                    (user_id,)
                )

                removed = True

            elif equipment[1] and equipment[1].lower() == canonical_name.lower():

                await db.execute(
                    """
                    UPDATE equipment
                    SET armor = NULL,
                        armor_durability = 0
                    WHERE user_id = ?
                    """,
                    (user_id,)
                )

                removed = True

            await db.commit()

        if not removed:

            await ctx.send(
                f"🧰 ┃ **{name}**, you don’t have that equipped."
            )

            return

        embed = discord.Embed(
            title="⚔️ ┃ Item Unequipped.",
            description=(
                f"**{name}** unequipped:\n\n"
                f"📦 ┃ **{canonical_name}**\n\n"
                "Your equipment slot is now empty."
            ),
            color=Colors.PRIMARY
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["eq"])
    async def equipment(
        self,
        ctx
    ):

        user_id = ctx.author.id
        name = ctx.author.display_name

        async with aiosqlite.connect(DB_PATH) as db:

            cursor = await db.execute(
                """
                SELECT
                    weapon,
                    armor,
                    weapon_durability,
                    armor_durability
                FROM equipment
                WHERE user_id = ?
                """,
                (user_id,)
            )

            data = await cursor.fetchone()

        if data is None:

            await ctx.send(
                f"⚔️ ┃ **{name}**, you have no equipment."
            )

            return

        weapon = data[0]
        armor = data[1]

        weapon_text = "None Equipped"

        if weapon:

            w = get_item(weapon)

            weapon_text = (
                f"{w['emoji']} **{weapon}**\n"
                f"{w['rarity']}\n"
                f"Attack : **+{w['attack']}**\n"
                f"Durability : **{data[2]}/{w['durability']}**"
            )

        armor_text = "None Equipped"

        if armor:

            a = get_item(armor)

            armor_text = (
                f"{a['emoji']} **{armor}**\n"
                f"{a['rarity']}\n"
                f"Defense : **+{a['defense']}**\n"
                f"Durability : **{data[3]}/{a['durability']}**"
            )

        embed = discord.Embed(
            title=f"🧰 ┃ {name}’s Equipment",
            color=Colors.WARNING
        )

        embed.add_field(
            name="⚔️ ┃ Weapon",
            value=weapon_text,
            inline=False
        )

        embed.add_field(
            name="🛡️ ┃ Armor",
            value=armor_text,
            inline=False
        )


        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(
        Equipment(bot)
    )