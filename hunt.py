import discord
import random
import time
import aiosqlite

from discord.ext import commands

from utils.colors import Colors
from utils.items import ITEMS


DB_PATH = "data/database.db"



hunt_cooldowns = {}

HUNT_TIME = 10



class Hunt(commands.Cog):

    def __init__(self, bot):

        self.bot = bot



    @commands.command()
    async def hunt(self, ctx):

        user_id = ctx.author.id
        name = ctx.author.display_name



        async with aiosqlite.connect(DB_PATH) as db:

            cursor = await db.execute(
                """
                SELECT user_id
                FROM players
                WHERE user_id = ?
                """,
                (
                    user_id,
                )
            )

            player = await cursor.fetchone()



        if player is None:

            await ctx.send(
                f"**{name}**, create your account first with `poo start`."
            )

            return




        current_time = time.time()


        if user_id in hunt_cooldowns:


            remaining = (
                hunt_cooldowns[user_id]
                + HUNT_TIME
                - current_time
            )


            if remaining > 0:

                minutes = int(
                    remaining // 60
                )

                seconds = int(
                    remaining % 60
                )


                await ctx.send(
                    f"⏳ ┃ **{name}**, you must wait "
                    f"**{minutes}m {seconds}s** before hunting again."
                )

                return



        hunt_cooldowns[user_id] = current_time




        rarity_roll = random.random() * 100


        if rarity_roll <= 0.01:

            rarity = "🌈 Divine"


        elif rarity_roll <= 0.10:

            rarity = "🟡 Legendary"


        elif rarity_roll <= 2:

            rarity = "🟣 Epic"


        elif rarity_roll <= 10:

            rarity = "🔵 Rare"


        elif rarity_roll <= 30:

            rarity = "🟢 Uncommon"


        else:

            rarity = "⚪ Common"



        possible_items = []


        for item_name, item in ITEMS.items():

            if item.get("rarity") == rarity:

                possible_items.append(
                    item_name
                )


        if not possible_items:

            await ctx.send(
                "❌ ┃ No items found for this rarity."
            )

            return



        found_item = random.choice(
            possible_items
        )


        item_data = ITEMS[found_item]



        async with aiosqlite.connect(DB_PATH) as db:


            await db.execute(
                """
                INSERT INTO inventory
                (
                    user_id,
                    item_name,
                    amount
                )

                VALUES (?, ?, 1)

                ON CONFLICT(user_id,item_name)

                DO UPDATE SET amount = amount + 1
                """,
                (
                    user_id,
                    found_item
                )
            )


            await db.commit()


        embed = discord.Embed(

            title="🏹 ┃ Hunt Complete!",

            description=(

                f"**{name}** went exploring...\n\n"

                f"🎁 ┃ Congrats! You found :\n\n"

                f"{item_data['emoji']} "
                f"**{found_item}**\n"

                f"✨ ┃ Rarity : **{rarity}**\n\n"

                "Added to your inventory."

            ),

            color=Colors.SUCCESS

        )


        await ctx.send(
            embed=embed
        )





async def setup(bot):

    await bot.add_cog(
        Hunt(bot)
    )