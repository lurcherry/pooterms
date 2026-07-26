import discord
import aiosqlite

from discord.ext import commands

from utils.items import get_item


DB_PATH = "data/database.db"


class Consumable(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def use(self, ctx, *, args):

        parts = args.rsplit(" ", 1)

        if len(parts) == 2 and parts[1].isdigit():

            item_name = parts[0]
            quantity = int(parts[1])

        else:

            item_name = args
            quantity = 1

        user_id = ctx.author.id


        item = get_item(item_name)

        if item is None or item.get("type") != "potion":

            await ctx.send(
                "❌ ┃ That is not a usable potion."
            )

            return


        heal = item.get("heal", 0) * quantity


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

            potion = await cursor.fetchone()


            if potion is None or potion[0] <= 0:

                await ctx.send(
                    f"❌ ┃ Poor thing, you do not have **{item_name}**."
                )

                return


            cursor = await db.execute(
                """
                SELECT hp
                FROM players
                WHERE user_id = ?
                """,
                (user_id,)
            )

            player = await cursor.fetchone()


            if player is None:

                await ctx.send(
                    "❌ ┃ You do not have a POO account."
                )

                return


            old_hp = player[0]
            new_hp = min(
                old_hp + heal,
                100
            )


            await db.execute(
                """
                UPDATE players
                SET hp = ?
                WHERE user_id = ?
                """,
                (
                    new_hp,
                    user_id
                )
            )


            await db.execute(
                """
                UPDATE inventory
                SET amount = amount - ?
                WHERE user_id = ?
                AND LOWER(item_name) = LOWER(?)
                """,
                (
                    quantity,
                    user_id,
                    item_name
                )
            )


            await db.commit()


        await ctx.send(
            f"🧪 ┃ **{ctx.author.display_name}** used "
            f"{item.get('emoji')} **{item_name}**!\n\n"
            f"❤️ ┃ HP : **{old_hp} → {new_hp}**\n"
            f"💚 ┃ Healed : **+{new_hp - old_hp} HP**"
        )


async def setup(bot):

    await bot.add_cog(
        Consumable(bot)
    )