import discord
import aiosqlite

from discord.ext import commands


DB_PATH = "data/database.db"


class Profile(commands.Cog):

    def __init__(
        self,
        bot
    ):

        self.bot = bot

    @commands.command(
        aliases=[
            "prof",
            "me"
        ]
    )
    async def profile(
        self,
        ctx,
        member: discord.Member = None
    ):

        if member is None:

            member = ctx.author


        async with aiosqlite.connect(
            DB_PATH
        ) as db:

            cursor = await db.execute(
                """
                SELECT
                    coins,
                    level,
                    experience,
                    hp,
                    rank,
                    stars,
                    wins,
                    losses,
                    daily_streak,
                    battle_result
                FROM players
                WHERE user_id = ?
                """,
                (
                    member.id,
                )
            )

            player = await cursor.fetchone()


            if player is None:

                await ctx.send(

                    "❌ ┃ That player doesn’t have a POO account."

                )

                return


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
                (
                    member.id,
                )
            )

            equipment = await cursor.fetchone()

        weapon = "No weapon equipped."
        armor = "No armor equipped."
        weapon_durability = 0
        armor_durability = 0

        if equipment:

            if equipment[0]:
                weapon = equipment[0]
                weapon_durability = equipment[2]


            if equipment[1]:
                armor = equipment[1]
                armor_durability = equipment[3]

        coins = player[0]
        level = player[1]
        experience = player[2]
        hp = player[3]
        rank = player[4]
        stars = player[5]
        wins = player[6]
        losses = player[7]

        total_battles = wins + losses

        if total_battles == 0:

            win_rate = 0

        else:

            win_rate = round(

                (wins / total_battles) * 100

            )
    
        daily_streak = player[8]
        battle_result = player[9]

        if battle_result == "up":

            arrow = " 🔺"

        elif battle_result == "down":

            arrow = " 🔻"

        else:

            arrow = ""

        if battle_result == "up":

            status = "📈 ┃ Rank Increased"

        elif battle_result == "down":

            status = "📉 ┃ Rank Decreased"

        else:

            status = "➖ ┃ No Rank"

        star_bar = (
            "⭐" * stars
            +
            "☆" * (5 - stars)
        )

        hp_bar = self.create_hp_bar(
            hp
        )

        exp_bar = self.create_exp_bar(
            experience,
            level
        )

        required_exp = level * 100

        exp_percent = round(

            (experience / required_exp) * 100

        )


        embed = discord.Embed(

            title=f"👤 ┃ {member.display_name}’s Profile",

            color=discord.Color.from_rgb(
                255,
                192,
                203
            )

        )

        embed.set_thumbnail(

            url=member.display_avatar.url

        )

        embed.add_field(

            name=f"💰 ┃ Crap Cash : {coins:,}",

            value=" ",

            inline=False

        )

        embed.add_field(

            name=" ",

            value=" ",

            inline=False

        )

        embed.add_field(

            name="🎖️ ┃ Rank",

            value=(
                f"{rank}\n"
                f"{star_bar}{arrow}"
            ),

            inline=False

        )

        embed.add_field(

            name=" ",

            value=" ",

            inline=False

        )

        embed.add_field(

            name="📋 ┃ Last Battle",

            value=status,

            inline=False

        )

        embed.add_field(

            name=f"🌟 Level : {level}",

            value="\u200b",

            inline=False

        )


        embed.add_field(

            name="❤️ ┃ Health",

            value=(
                f"{hp_bar}\n"
                f"{hp} / 100"
            ),

            inline=False

        )

        embed.add_field(

            name="⚡ ┃ Experience",

            value=(
                f"{exp_bar}\n"
                f"{experience} / {required_exp}"
                f"({exp_percent}%)"
            ),

            inline=False

        )

        embed.add_field(

            name=" ",

            value=" ",

            inline=False

        )

        embed.add_field(

            name="⚔️ ┃ Record",

            value=(
                f"🏆 ┃ Wins : **{wins}**\n"
                f"💀 ┃ Losses : **{losses}**\n"
                f"📊 ┃ Win Rate : **{win_rate}%**"
            ),

            inline=False

        )

        embed.add_field(

            name=" ",

            value=" ",

            inline=False

        )


        embed.add_field(

            name="🔥 ┃ Daily Streak",

            value=f"{daily_streak} Days",

            inline=False

        )

        embed.add_field(

            name=" ",

            value=" ",

            inline=False

        )

        embed.add_field(

            name="🧰 ┃ Equipment",

            value=(
                f"⚔️ ┃ {weapon}\n"
                f"🔧 ┃ Durability : **{weapon_durability}/100**\n"
                f"🛡️ ┃ {armor}\n"
                f"🔧 ┃ Durability : **{armor_durability}/100**"
            ),

            inline=False

        )

        await ctx.send(
            embed=embed
        )

    def create_hp_bar(
        self,
        hp
    ):

        filled = max(
            0,
            min(
                10,
                hp // 10
            )
        )

        return (
            "🟥" * filled
            +
            "⬜" * (10 - filled)
        )


    def create_exp_bar(
        self,
        experience,
        level
    ):

        required = max(
            level * 100,
            1
        )

        filled = int(
            min(
                experience / required,
                1
                ) * 10
        )

        filled = max(
            0,
            min(
                10,
                filled
            )
        )

        return (
            "🟩" * filled
            +
            "⬜" * (10 - filled)
        )

async def setup(bot):
    await bot.add_cog(
        Profile(bot)
    )