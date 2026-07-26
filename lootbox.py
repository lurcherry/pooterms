import discord
import random
import aiosqlite

from discord.ext import commands

from utils.items import (
    ITEMS,
    LOOTBOX_POOL,
    get_item
)

from utils.inventory import add_inventory_item

DB_PATH = "data/database.db"


class Lootbox(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def open(self, ctx, *, lootbox_input):

        user_id = ctx.author.id

        amount = 1

        parts = lootbox_input.rsplit(" ", 1)

        if len(parts) == 2 and parts[1].isdigit():

            lootbox_name = parts[0]
            amount = int(parts[1])

        else:

            lootbox_name = lootbox_input

        if amount < 1:

            await ctx.send(
                "❌ ┃ Amount must be at least **1**."
            )

            return

        real_name = None

        for item_name, item_data in ITEMS.items():

            if (
                item_data.get("type") == "lootbox"
                and item_name.lower() == lootbox_name.lower()
            ):

                real_name = item_name
                break

        if real_name is None:

            await ctx.send(
                "❌ ┃ That lootbox doesn’t exist."
            )

            return

        lootbox_name = real_name

        async with aiosqlite.connect(DB_PATH) as db:

            cursor = await db.execute(
                """
                SELECT amount
                FROM inventory
                WHERE user_id = ?
                AND LOWER(item_name) = LOWER(?)
                """,
                (
                    user_id,
                    lootbox_name
                )
            )

            box = await cursor.fetchone()

            if box is None or box[0] < amount:

                await ctx.send(
                    f"❌ ┃ You don’t have **{amount}x {lootbox_name}**."
                )

                return

            await db.execute(
                """
                UPDATE inventory
                SET amount = amount - ?
                WHERE user_id = ?
                AND LOWER(item_name) = LOWER(?)
                """,
                (
                    amount,
                    user_id,
                    lootbox_name
                )
            )


            await db.execute(
                """
                DELETE FROM inventory
                WHERE user_id = ?
                AND LOWER(item_name) = LOWER(?)
                AND amount <= 0
                """,
                (
                    user_id,
                    lootbox_name
                )
            )


            await db.commit()

        pool = LOOTBOX_POOL[lootbox_name]

        obtained = {}

        for _ in range(amount):

            chosen_rarity = random.choices(
                population=list(pool.keys()),
                weights=list(pool.values()),
                k=1
            )[0]

            possible_rewards = [

                item_name

                for item_name, item_data in ITEMS.items()

                if (
                    item_data.get("type") != "lootbox"
                    and item_data.get("rarity") == chosen_rarity
                )

            ]

            if not possible_rewards:
                continue

            reward = random.choice(possible_rewards)

            obtained[reward] = obtained.get(
                reward,
                0
            ) + 1

        for reward, quantity in obtained.items():

            await add_inventory_item(
                user_id,
                reward,
                quantity
            )

        lines = []

        for reward, quantity in obtained.items():

            item = get_item(reward)

            emoji = item.get("emoji", "📦")

            rarity = item.get("rarity", "⚪ Common")

            lines.append(
                f"{emoji} **{reward}** ×{quantity}\n"
                f"└ {rarity}"
            )

        box_text = (
            lootbox_name
            if amount == 1
            else f"{lootbox_name}s"
        )

        embed = discord.Embed(
            title="🎁 ┃ Lootbox Opened",
            color=discord.Color.gold()
        )

        embed.description = (
            f"**{ctx.author.display_name}** opened "
            f"**{amount} {box_text}**!"
        )

        embed.add_field(
            name="✨ Rewards",
            value="\n\n".join(lines) if lines else "Nothing...",
            inline=False
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Lootbox(bot))