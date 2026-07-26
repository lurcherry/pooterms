import discord
import random
import aiosqlite

from datetime import datetime, timedelta
from discord.ext import commands
from utils.leveling import add_exp
from utils.colors import Colors
from utils.items import ITEMS
from utils.inventory import add_inventory_item


DB_PATH = "data/database.db"


class Daily(commands.Cog):

    def __init__(self, bot):

        self.bot = bot



    @commands.command()
    async def daily(self, ctx):

        user_id = ctx.author.id
        name = ctx.author.display_name



        async with aiosqlite.connect(DB_PATH) as db:


            cursor = await db.execute(
                """
                SELECT coins,
                       daily_streak,
                       last_daily,
                       level

                FROM players

                WHERE user_id = ?

                """,
                (user_id,)
            )


            player = await cursor.fetchone()



        if player is None:

            await ctx.send(
                f"❌ ┃ **{name}**, create your account first with `poo start`."
            )

            return
        
        
        
        coins, streak, last_daily, level = player


        now = datetime.now()



        if last_daily:


            last_time = datetime.fromisoformat(
                last_daily
            )


            cooldown = last_time + timedelta(
                hours=24
            )


            if now < cooldown:


                remaining = cooldown - now


                hours = remaining.seconds // 3600

                minutes = (
                    remaining.seconds % 3600
                ) // 60


                await ctx.send(

                    f"⏰ ┃ **{name}**, whoa, already?\n"

                    f"📦 ┃ Your **Daily Loot Box** is not ready yet.\n"

                    f"⌛ ┃Come back in **{hours}h {minutes}m**."

                )

                return
            

        cash_reward = 500 * level

        exp_reward = random.randint(50, 150)

        lootbox_reward = "Lucky Lootbox"



        streak += 1



        async with aiosqlite.connect(DB_PATH) as db:


            await db.execute(
                """
                UPDATE players
                SET coins = coins + ?,
                    daily_streak = ?,
                    last_daily = ?
                WHERE user_id = ?
                """,
                (
                    cash_reward,
                    streak,
                    now.isoformat(),
                    user_id
                )
            )

            await db.commit()



        await add_inventory_item(
            user_id,
            lootbox_reward,
            1
        )


        await add_exp(
            user_id,
            exp_reward
        )


        reward_text = (

                f"💰 ┃ +{cash_reward:,} Crap Cash\n"
                f"⚡ ┃ +{exp_reward} EXP\n"
                f"📦 ┃ {lootbox_reward} ×1"

            )


        message = (
            f"🎁 ┃ **{name}**, you survived another day! POO decided to reward you.\n"
            f"{reward_text}\n"
            f"🔥 ┃ Daily Streak : **{streak}**\n"
            f"⏳ ┃ Your next daily is in **23h 59m**."

        )


        await ctx.send(
            message
        )




async def setup(bot):

    await bot.add_cog(
        Daily(bot)
    )