import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

from utils.database import initialize_database


load_dotenv()


TOKEN = os.getenv("TOKEN")


if TOKEN is None:
    raise RuntimeError(
        "TOKEN was not found in your .env file."
    )

class PooBot(commands.Bot):

    def __init__(self):

        intents = discord.Intents.default()

        intents.message_content = True


        super().__init__(
            command_prefix=["poo ", "p "],
            intents=intents,
            help_command=None,
            case_insensitive=True
        )


    async def setup_hook(self):

        print("Initializing database...")

        await initialize_database()


        print("Loading cogs...")


        for filename in os.listdir("cogs"):

            if filename.endswith(".py") and filename != "__init__.py":


                extension = f"cogs.{filename[:-3]}"


                try:

                    await self.load_extension(extension)

                    print(f"Loaded {extension}")


                except Exception as e:

                    print(f"Failed loading {extension}")

                    print(e)

    async def get_context(self, message, *, cls=commands.Context):

        if message.content:

            lower = message.content.lower()

            if lower.startswith("poo "):

                message.content = "poo " + message.content[4:]

            elif lower.startswith("p "):

                message.content = "p " + message.content[2:]

        return await super().get_context(message, cls=cls)



bot = PooBot()

@bot.event
async def on_ready():

    print("\n" + "=" * 45)

    print("POO is now online!")

    print("=" * 45)

    print(f"Logged in as : {bot.user}")

    print(f"Bot ID       : {bot.user.id}")

    print(f"Prefix       : poo ")

    print("=" * 45 + "\n")




@bot.event
async def on_command_error(
    ctx,
    error
):


    if isinstance(
        error,
        commands.CommandNotFound
    ):

        return



    if isinstance(
        error,
        commands.MissingRequiredArgument
    ):

        await ctx.send(

            f"❌ ┃ **{ctx.author.display_name}**, POO detected missing information.\n"

            f"POO is confused... you did not tell me what to do.\n\n"

            f"Use : `poo {ctx.command.name} {ctx.command.signature}`"

        )


        return




    if isinstance(
        error,
        commands.CommandOnCooldown
    ):


        seconds = round(
            error.retry_after
        )


        await ctx.send(

            f"⏳ ┃ Woah! **{ctx.author.display_name}**, slow down!\n"

            f"Try again in **{seconds} seconds**."

        )


        return




    if isinstance(
        error,
        commands.MissingPermissions
    ):


        await ctx.send(

            f"🚫 ┃ **{ctx.author.display_name}**, you don not have permission to use that command."

        )


        return



    raise error




bot.run(TOKEN)