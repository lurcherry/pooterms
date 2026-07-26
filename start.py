import discord
import aiosqlite

from discord.ext import commands

from utils.colors import Colors
from utils.messages import Messages


DB_PATH = "data/database.db"



class Start(commands.Cog):

    def __init__(self, bot):

        self.bot = bot



    @commands.command()
    async def start(self, ctx):

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


            existing = await cursor.fetchone()



        if existing:

            await ctx.send(
                Messages.already_registered(name)
            )

            return



        embed = discord.Embed( 

            title="Welcome to POO!",

            description=(

                f"📜 ┃ **POO Code Of Conduct**\n\n"

                "Please take a moment to read these guidelines to help keep "
                "**POO safe, fair, and enjoyable** for everyone. "
                "By being part of **POO**, you agree to follow these rules "
                "and help maintain a **positive experience** for all players.\n\n"


                "🚫 ┃ **No Cheating Or Exploiting.**\n"
                "Do not use **hacks, cheats, or exploits** to gain unfair advantages. "
                "If you discover a bug, please **report it** instead of abusing it.\n\n"

                "⚙️ ┃ **Do Not Abuse Commands.**\n"
                "Avoid **command spam**, automation, or abusing bot systems. "
                "Use POO commands properly so everyone can enjoy the game fairly.\n\n"

                "🫱🏼‍🫲🏾 ┃ **Respect Other Players.**\n"
                "Treat other players with **respect and fairness**. "
                "Avoid harassment, toxicity, or actions that intentionally ruin "
                "someone else’s experience.\n\n"

                "⚖️ ┃ **Keep Trading Fair.**\n"
                "Do not sell **accounts, items, or in-game progress for real money**. "
                "Keep all trades safe and follow POO’s guidelines.\n\n"

                "🎮 ┃ **Play Fair And Enjoy The Game.**\n"
                "Do not use unfair methods to gain **items, currency, or progress**. "
                "Respect the game and help keep POO a **fun experience** for everyone.\n\n"


                "Click **Agree** to accept these rules "
                "and create your account."

            ),

            color=Colors.PRIMARY

        )


        embed.set_footer(

            text="You have 60 seconds to choose."

        )



        view = StartButtons(
            ctx.author
        )


        message = await ctx.send(

            embed=embed,

            view=view

        )


        view.message = message

class StartButtons(discord.ui.View):

    def __init__(self, author):

        super().__init__(
            timeout=60
        )

        self.author = author

        self.message = None



    async def interaction_check(
        self,
        interaction
    ):

        if interaction.user.id != self.author.id:


            await interaction.response.send_message(

                "❌ ┃ This confirmation is not for you.",

                ephemeral=True

            )


            return False



        return True




    @discord.ui.button(

        label="Agree",

        emoji="🟢",

        style=discord.ButtonStyle.success

    )
    async def agree(

        self,

        interaction,

        button

    ):



        await interaction.response.defer()



        user_id = self.author.id

        username = self.author.display_name




        async with aiosqlite.connect(DB_PATH) as db:



            await db.execute(

                """

                INSERT INTO players

                (

                    user_id,

                    username,

                    coins

                )

                VALUES (?, ?, ?)

                """,

                (

                    user_id,

                    username,
                    
                    1200

                )

            )



            await db.execute(

                """

                INSERT INTO equipment

                (

                    user_id

                )

                VALUES (?)

                """,

                (

                    user_id,

                )

            )



            await db.commit()

            embed = discord.Embed(

                title="Welcome to POO!",

                description=(

                    f"**You finally made it!**\n"
                    "Congratulations! You are now officially part of **POO**.\n\n"

                    "🎁 ┃ **Starter Rewards**\n"
                    "💰 ┃ Starting Crap Cash : **1,200**\n"
                    "⭐ ┃ Level : **1**\n"
                    "❤️ ┃ HP : **100**\n\n"

                    "📜 ┃ **Your First Commands**\n"
                    "`poo profile` — View your stats and progress\n"
                    "`poo fight` — Fight monsters and earn rewards\n"
                    "`poo help` — Guide and map of POO\n\n"

                    "⚔️ ┃ **Have fun, do not cheat!**\n"
                    "and please try not to embarrass yourself."

                ),

                color=Colors.SUCCESS
            )



        await interaction.edit_original_response(
            embed=embed,
            view=None
            )



        self.stop()

    @discord.ui.button(

        label="Decline",

        emoji="🔴",

        style=discord.ButtonStyle.danger

    )
    async def decline(

        self,

        interaction,

        button

    ):


        await interaction.response.defer()



        name = self.author.display_name



        await interaction.edit_original_response(

            content=(

                f"❌ ┃ **{name}**, account creation cancelled.\n"

                "You can use `poo start` anytime if you change your mind."

            ),

            embed=None,

            view=None

        )



        self.stop()




    async def on_timeout(self):


        if self.message:


            await self.message.edit(

                content=(

                    "⏰ ┃ Account creation timed out.\n"

                    "Use `poo start` again when you are ready."

                ),

                embed=None,

                view=None

            )





async def setup(bot):

    await bot.add_cog(

        Start(bot)

    )
