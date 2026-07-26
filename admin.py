import discord
import aiosqlite

from discord.ext import commands

from utils.colors import Colors


DB_PATH = "data/database.db"

OWNER_ID = 898313006100914237


class Admin(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    def is_owner(self, ctx):

        return ctx.author.id == OWNER_ID



    @commands.command()
    async def addcoins(
        self,
        ctx,
        member: discord.Member,
        amount: int
    ):


        if not self.is_owner(ctx):

            embed = discord.Embed(

                title="❌ ┃ Access Denied",

                description=(

                    "Aba ayos, admin abuse lang 😭"

                ),

                color=Colors.ERROR

            )

            await ctx.send(embed=embed)

            return



        if amount <= 0:

            await ctx.send(
                "❌ ┃ Enter a valid amount."
            )

            return



        async with aiosqlite.connect(DB_PATH) as db:

            await db.execute(

                """
                UPDATE players

                SET coins = coins + ?

                WHERE user_id = ?

                """,

                (
                    amount,
                    member.id
                )

            )

            await db.commit()



        embed = discord.Embed(

            title="ADMIN ABUSE CASHAWT",

            description=(

                f"**{member.display_name}** received :\n\n"

                f"**{amount:,} Crap Cash**\n\n"

                "From **SUGAR MOMMY JEN**."

            ),

            color=Colors.SUCCESS

        )


        await ctx.send(

            embed=embed

        )




    @commands.command()
    async def additem(
        self,
        ctx,
        member: discord.Member,
        *,
        item_name
    ):


        if not self.is_owner(ctx):

            embed = discord.Embed(

                title="❌ ┃ Access Denied",

                description=(

                    "Only the creator of POO "
                    "can use admin commands."

                ),

                color=Colors.ERROR

            )

            await ctx.send(embed=embed)

            return



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

                ON CONFLICT(user_id, item_name)

                DO UPDATE SET amount = amount + 1

                """,

                (
                    member.id,
                    item_name
                )

            )

            await db.commit()



        embed = discord.Embed(

            title="ADMIN ABUSE SHABU",

            description=(

                f"**{member.display_name}** received :\n\n"

                f"**{item_name}**\n\n"

                "From **SUGAR MOMMY JEN**."

            ),

            color=Colors.SUCCESS

        )


        await ctx.send(

            embed=embed

        )




    @commands.command()
    async def setlevel(
        self,
        ctx,
        member: discord.Member,
        level: int
    ):


        if not self.is_owner(ctx):

            await ctx.send(

                "❌ ┃ Only Sugar Mommy Jen can use this."

            )

            return



        if level < 1:

            await ctx.send(

                "❌ ┃ Level must be above 0."

            )

            return



        async with aiosqlite.connect(DB_PATH) as db:

            await db.execute(

                """
                UPDATE players

                SET level = ?

                WHERE user_id = ?

                """,

                (
                    level,
                    member.id
                )

            )

            await db.commit()



        embed = discord.Embed(

            title="ADMIN ABUSE LEBEL",

            description=(

                f"**{member.display_name}**\n\n"

                f"Level changed to **{level}**\n\n"

                "From **SUGAR MOMMY JEN**."

            ),

            color=Colors.PRIMARY

        )


        await ctx.send(

            embed=embed

        )



async def setup(bot):

    await bot.add_cog(

        Admin(bot)

    )