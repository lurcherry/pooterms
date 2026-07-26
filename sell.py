import discord
import aiosqlite

from discord.ext import commands

from utils.colors import Colors
from utils.items import get_item
from utils.messages import Messages


DB_PATH = "data/database.db"


class Sell(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    async def sell(self, ctx, *, item_name=None):

        user_id = ctx.author.id
        name = ctx.author.display_name



        if item_name is None:

            await ctx.send(
                f"💰 ┃ **{name}**, tell me what item you want to sell."
            )

            return



        async with aiosqlite.connect(DB_PATH) as db:


            cursor = await db.execute(
                """
                SELECT amount, item_name
                FROM inventory

                WHERE user_id = ?
                AND LOWER(item_name) = LOWER(?)

                """,
                (
                    user_id,
                    item_name
                )
            )


            item = await cursor.fetchone()



        if item is None:

            await ctx.send(
                f"🧰 ┃ **{name}**, you don’t have that item."
            )

            return



        amount = item[0]
        item_name = item[1]


        data = get_item(
            item_name
        )


        if data is None:

            await ctx.send(
                f"❌ ┃ **{name}**, that item cannot be sold."
            )

            return



        total_price = (
            data["sell"] * amount
        )



        async with aiosqlite.connect(DB_PATH) as db:


            await db.execute(
                """
                DELETE FROM inventory

                WHERE user_id = ?
                AND item_name = ?

                """,
                (
                    user_id,
                    item_name
                )
            )



            await db.execute(
                """
                UPDATE players

                SET coins = coins + ?

                WHERE user_id = ?

                """,
                (
                    total_price,
                    user_id
                )
            )


            await db.commit()



        embed = discord.Embed(

            title="💰 ┃ Item Sold!",

            description=(

                f"**{name}**, you sold :\n\n"

                f"{data['emoji']} **{item_name}** ×{amount}\n\n"

                f"💰 ┃ Earned : **{total_price:,} Coins**\n\n"

                "Your wallet is smiling again."

            ),

            color=Colors.SUCCESS

        )


        await ctx.send(
            embed=embed
        )



    @commands.command(
        name="sellall"
    )
    async def sell_all(self, ctx):

        user_id = ctx.author.id
        name = ctx.author.display_name



        async with aiosqlite.connect(DB_PATH) as db:


            cursor = await db.execute(
                """
                SELECT item_name, amount

                FROM inventory

                WHERE user_id = ?

                """,
                (user_id,)
            )


            items = await cursor.fetchall()



        if not items:

            await ctx.send(
                f"🧰 ┃ **{name}**, you poor thing, your inventory is empty."
            )

            return



        total = 0


        async with aiosqlite.connect(DB_PATH) as db:


            for item_name, amount in items:


                item = get_item(
                    item_name
                )


                if item:

                    total += (
                        item["sell"] * amount
                    )



            await db.execute(
                """
                DELETE FROM inventory

                WHERE user_id = ?

                """,
                (user_id,)
            )


            await db.execute(
                """
                UPDATE players

                SET coins = coins + ?

                WHERE user_id = ?

                """,
                (
                    total,
                    user_id
                )
            )


            await db.commit()



        await ctx.send(

            f"💰 ┃ **{name}**, you sold your inventory!\n"
            f"You earned **{total:,} Crap Cash**."

        )



async def setup(bot):

    await bot.add_cog(
        Sell(bot)
    )