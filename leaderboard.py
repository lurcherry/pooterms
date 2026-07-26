import discord
import aiosqlite

from discord.ext import commands


DB_PATH = "data/database.db"

class Leaderboard(commands.Cog):

    def __init__(
        self,
        bot
    ):

        self.bot = bot

    @commands.command(
        aliases=["lb"]
    )
    async def leaderboard(
        self,
        ctx
    ):

        async with aiosqlite.connect(
            DB_PATH
        ) as db:

            cursor = await db.execute(
                """
                SELECT
                    username,
                    wins,
                    rank,
                    stars
                FROM players
                ORDER BY wins DESC
                LIMIT 10
                """
            )

            players = await cursor.fetchall()


        if not players:

            await ctx.send(
                "🏆 ┃ No players yet."
            )

            return


        embed = discord.Embed(
            title="🏆 ┃ POO Leaderboard",
            color=discord.Color.gold()
        )


        text = ""


        position = 1


        for player in players:

            username, wins, rank, stars = player


            star_display = (
                "⭐" * stars +
                "☆" * (5 - stars)
            )


            text += (
                f"**{position}. {username}**\n"
                f"{rank} {star_display}\n"
                f"🏆 Wins : **{wins}**\n\n"
            )


            position += 1


        embed.description = text


        await ctx.send(
            embed=embed
        )

async def setup(bot):

    await bot.add_cog(
        Leaderboard(bot)
    )