import discord
from discord.ext import commands

from utils.colors import Colors


class HelpView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=300)

        self.remove_item(self.back_button)

    def main_embed(self):
        embed = discord.Embed(
            title="📖 ┃ POO Help Center",
            description=(
                "Welcome to **POO BOT!**\n\n"
                "Choose a category below to view "
                "all available commands."
            ),
            color=Colors.PRIMARY
        )

        embed.add_field(
            name="👤 Account",
            value=(
                "`poo start`\n"
                "`poo profile`\n"
                "`poo daily`\n"
                "`poo cash`\n"
                "`poo give`"
            ),
            inline=True
        )

        embed.add_field(
            name="⚔️ Combat",
            value=(
                "`poo hunt`\n"
                "`poo fight`\n"
                "`poo battle`"
            ),
            inline=True
        )

        embed.add_field(
            name="🧰 Inventory",
            value=(
                "`poo inv` / `inventory`\n"
                "`poo equipment`\n"
                "`poo equip`\n"
                "`poo unequip`\n"
                "`poo open`\n"
                "`poo use`"
            ),
            inline=True
        )

        embed.add_field(
            name="🛒 Shop",
            value=(
                "`poo shop`\n"
                "`poo buy`\n"
                "`poo sell`"
            ),
            inline=True
        )

        embed.add_field(
            name="🎲 Casino",
            value=(
                "`poo cf` / `coinflip`\n"
                "`poo s` / `slots`\n"
                "`poo bj` / `blackjack`"
            ),
            inline=True
        )

        embed.add_field(
            name="❓ General",
            value=(
                "`poo help`\n"
                "`poo lb` / `leaderboard`"
            ),
            inline=True
        )

        return embed

    def show_category_view(self):
        """Helper to ensure the back button is present when viewing a category."""
        if self.back_button not in self.children:
            self.add_item(self.back_button)

    def show_main_view(self):
        """Helper to remove the back button when returning to the main menu."""
        if self.back_button in self.children:
            self.remove_item(self.back_button)

    @discord.ui.button(
        label="👤 Account",
        style=discord.ButtonStyle.secondary,
        row=0
    )
    async def account(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        self.show_category_view()
        embed = discord.Embed(
            title="👤 ┃ Account Commands",
            description=(
                "`poo start`\n"
                "Create your POO account.\n\n"
                "`poo profile`\n"
                "View your profile.\n\n"
                "`poo daily`\n"
                "Claim your daily lootbox.\n\n"
                "`poo cash`\n"
                "Check your Crap Cash.\n\n"
                "`poo give @user <amount>`\n"
                "Send Crap Cash to another player."
            ),
            color=Colors.PRIMARY
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(
        label="⚔️ Combat",
        style=discord.ButtonStyle.secondary,
        row=0
    )
    async def combat(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        self.show_category_view()
        embed = discord.Embed(
            title="⚔️ ┃ Combat Commands",
            description=(
                "`poo hunt`\n"
                "Hunt to find Crap Cash, items, consumables, and lootboxes.\n\n"
                "`poo fight`\n"
                "Fight monsters to earn Crap Cash, EXP, and loot.\n\n"
                "`poo battle @user`\n"
                "Challenge another player to a PvP battle."
            ),
            color=Colors.PRIMARY
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(
        label="🧰 Inventory",
        style=discord.ButtonStyle.secondary,
        row=0
    )
    async def inventory(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        self.show_category_view()
        embed = discord.Embed(
            title="🧰 ┃ Inventory Commands",
            description=(
                "`poo inventory` (`poo inv`)\n"
                "View everything you own.\n\n"
                "`poo equipment`\n"
                "View equipped gear.\n\n"
                "`poo equip <item>`\n"
                "Equip a weapon or armor.\n\n"
                "`poo unequip <item>`\n"
                "Remove equipped gear.\n\n"
                "`poo open <lootbox>`\n"
                "Open earned lootboxes for rewards.\n\n"
                "`poo use <potion>`\n"
                "Use a consumable item."
            ),
            color=Colors.PRIMARY
        )
        await interaction.response.edit_message(embed=embed, view=self)

    # Row 1 Buttons
    @discord.ui.button(
        label="🛒 Shop",
        style=discord.ButtonStyle.secondary,
        row=1
    )
    async def shop(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        self.show_category_view()
        embed = discord.Embed(
            title="🛒 ┃ Shop Commands",
            description=(
                "`poo shop`\n"
                "Browse items available for purchase.\n\n"
                "`poo buy <item>`\n"
                "Buy an item from the shop.\n\n"
                "`poo sell <item>`\n"
                "Sell an item from your inventory for Crap Cash."
            ),
            color=Colors.PRIMARY
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(
        label="🎲 Casino",
        style=discord.ButtonStyle.secondary,
        row=1
    )
    async def casino(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        self.show_category_view()
        embed = discord.Embed(
            title="🎲 ┃ Casino Commands",
            description=(
                "`poo coinflip <amount> <heads/tails>` (`poo cf`)\n"
                "Flip a coin and test your luck.\n\n"
                "`poo slots <amount>` (`poo s`)\n"
                "Spin the slot machine for big rewards.\n\n"
                "`poo blackjack` (`poo bj`)\n"
                "Play Blackjack against the dealer."
            ),
            color=Colors.PRIMARY
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(
        label="❓ General",
        style=discord.ButtonStyle.secondary,
        row=1
    )
    async def general(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        self.show_category_view()
        embed = discord.Embed(
            title="❓ ┃ General Commands",
            description=(
                "`poo help`\n"
                "Open this help menu.\n\n"
                "`poo leaderboard` (`poo lb`)\n"
                "Check the top ranks in the leaderboard."
            ),
            color=Colors.PRIMARY
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(
        label="⬅️ Back",
        style=discord.ButtonStyle.secondary,
        row=2
    )
    async def back_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        self.show_main_view()
        await interaction.response.edit_message(
            embed=self.main_embed(),
            view=self
        )


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        view = HelpView()

        await ctx.send(
            embed=view.main_embed(),
            view=view
        )


async def setup(bot):
    await bot.add_cog(Help(bot))