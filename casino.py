import discord
import random
import asyncio
import aiosqlite
from discord.ext import commands

from utils.colors import Colors
from utils.messages import Messages

DB_PATH = "data/database.db"
MAX_BET = 250000


class BlackjackView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.choice = None
        self.message = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ ┃ This is not your blackjack game.",
                ephemeral=True
            )
            return False
        return True

    def disable_buttons(self):
        for button in self.children:
            button.disabled = True

    async def on_timeout(self):
        self.choice = None
        self.disable_buttons()
        if self.message:
            try:
                await self.message.edit(view=self)
            except (discord.NotFound, discord.HTTPException):
                pass

    @discord.ui.button(label="Hit", emoji="🃏", style=discord.ButtonStyle.success)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choice = "hit"
        await interaction.response.defer()
        self.disable_buttons()
        self.stop()

    @discord.ui.button(label="Stand", emoji="🛑", style=discord.ButtonStyle.danger)
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choice = "stand"
        await interaction.response.defer()
        self.disable_buttons()
        self.stop()


class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_coins(self, user_id):
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT coins FROM players WHERE user_id = ?", (user_id,))
            data = await cursor.fetchone()
        return data[0] if data else None

    async def add_coins(self, user_id, amount):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("UPDATE players SET coins = coins + ? WHERE user_id = ?", (amount, user_id))
            await db.commit()

    async def remove_coins(self, user_id, amount):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("UPDATE players SET coins = coins - ? WHERE user_id = ?", (amount, user_id))
            await db.commit()

    # --- COIN FLIP COMMAND ---
    @commands.command(name="cf")
    async def coinflip(self, ctx, amount: str, choice: str):
        user_id = ctx.author.id
        name = ctx.author.display_name
        coins = await self.get_coins(user_id)

        if coins is None:
            await ctx.send("❌ ┃ **Oops! You don’t have an account.** Try `poo start` to create one!")
            return

        if coins <= 0:
            await ctx.send(f"💸 ┃ **{name}**, you poor thing! You do not have enough **Crap Cash**.")
            return

        if amount.lower() == "all":
            bet = min(coins, MAX_BET)
        else:
            try:
                bet = int(amount)
            except ValueError:
                await ctx.send("❌ ┃ Oops! That’s not it! Enter a valid number.")
                return

        if bet <= 0:
            await ctx.send("❌ ┃ Oops! Bet must be above **0 Crap Cash**.")
            return

        if bet > MAX_BET:
            await ctx.send(f"⚠️ ┃ Easy! Maximum bet is **{MAX_BET:,} Crap Cash**.")
            return

        if bet > coins:
            await ctx.send(f"💸 ┃ **{name}**, you need **{bet:,} Crap Cash** but only have **{coins:,}**.")
            return

        choice = choice.lower()
        if choice in ["h", "heads"]:
            choice = "Heads"
        elif choice in ["t", "tails"]:
            choice = "Tails"
        else:
            await ctx.send(
                "❌ ┃ Engk! Invalid choice!\nChoose `h` for **Heads** or `t` for **Tails**.\n\n"
                "Example : `poo cf 1000 h`"
            )
            return

        await self.remove_coins(user_id, bet)

        embed = discord.Embed(
            title="🪙 ┃ Coin Flip",
            description=f"**{name}** bet **{bet:,} Crap Cash** and chose **{choice}!**\n\n🪙 ┃ The coin is spinning...",
            color=Colors.WARNING
        )
        message = await ctx.send(embed=embed)
        await asyncio.sleep(1)

        result = random.choice(["Heads", "Tails"])

        if choice == result:
            reward = bet * 2
            await self.add_coins(user_id, reward)
            embed.description = (
                f"**{name}** bet **{bet:,} Crap Cash** and chose **{choice}!**\n\n"
                f"🪙 ┃ Coin landed on **{result}!**\n"
                f"🎉 ┃ **{name} won {reward:,} Crap Cash!**"
            )
            embed.color = Colors.SUCCESS
        else:
            embed.description = (
                f"**{name}** bet **{bet:,} Crap Cash** and chose **{choice}!**\n\n"
                f"🪙 ┃ Coin landed on **{result}!**\n"
                f"💀 ┃ **{name} lost {bet:,} Crap Cash.**"
            )
            embed.color = Colors.ERROR

        await message.edit(embed=embed)

    # --- SLOTS COMMAND ---
    @commands.command(aliases=["s"])
    async def slots(self, ctx, amount: str):
        user_id = ctx.author.id
        name = ctx.author.display_name
        coins = await self.get_coins(user_id)

        if coins is None:
            await ctx.send("❌ ┃ **Oops! You don’t have an account.** Try `poo start` to create one!")
            return

        if coins <= 0:
            await ctx.send(f"💸 ┃ **{name}**, you poor thing! You do not have enough **Crap Cash**.")
            return

        if amount.lower() == "all":
            bet = min(coins, MAX_BET)
        else:
            try:
                bet = int(amount)
            except ValueError:
                await ctx.send("❌ ┃ Oops! That’s not it! Enter a valid number.")
                return

        if bet <= 0:
            await ctx.send("❌ ┃ Oops! Bet must be above **0 Crap Cash**.")
            return

        if bet > MAX_BET:
            await ctx.send(f"⚠️ ┃ Easy! Maximum bet is **{MAX_BET:,} Crap Cash**.")
            return

        if bet > coins:
            await ctx.send(f"💸 ┃ **{name}**, you need **{bet:,} Crap Cash** but only have **{coins:,}**.")
            return

        await self.remove_coins(user_id, bet)

        symbols = ["🍒", "🍋", "🔔", "⭐", "💎", "🌈"]
        embed = discord.Embed(
            title="🎰 ┃ Slots",
            description=f"**{name}** bet **{bet:,} Crap Cash**\n\n🎰 ┃ The machine is spinning...",
            color=Colors.WARNING
        )
        message = await ctx.send(embed=embed)
        await asyncio.sleep(1)

        first = random.choice(symbols)
        embed.description = f"**{name}** bet **{bet:,} Crap Cash**\n\n🎰 ┃ {first} ❓ ❓"
        await message.edit(embed=embed)
        await asyncio.sleep(1)

        second = random.choice(symbols)
        embed.description = f"**{name}** bet **{bet:,} Crap Cash**\n\n🎰 ┃ {first} {second} ❓"
        await message.edit(embed=embed)
        await asyncio.sleep(1)

        third = random.choice(symbols)
        embed.description = f"**{name}** bet **{bet:,} Crap Cash**\n\n🎰 ┃ {first} {second} {third}"
        await message.edit(embed=embed)
        await asyncio.sleep(1)

        reward = 0
        if first == second == third:
            if first == "🌈":
                reward = bet * 10
            elif first == "💎":
                reward = bet * 5
            else:
                reward = bet * 3

        if reward > 0:
            await self.add_coins(user_id, reward)
            embed.description = (
                f"**{name}** bet **{bet:,} Crap Cash**\n\n"
                f"🎰 ┃ {first} {second} {third}\n\n"
                f"🎉 ┃ **{name} won {reward:,} Crap Cash!**"
            )
            embed.color = Colors.SUCCESS
        else:
            embed.description = (
                f"**{name}** bet **{bet:,} Crap Cash**\n\n"
                f"🎰 ┃ {first} {second} {third}\n\n"
                f"💀 ┃ **{name} lost {bet:,} Crap Cash.**"
            )
            embed.color = Colors.ERROR

        await message.edit(embed=embed)

    # --- BLACKJACK COMMAND ---
    @commands.command(aliases=["bj"])
    async def blackjack(self, ctx, amount: str):
        user_id = ctx.author.id
        name = ctx.author.display_name
        coins = await self.get_coins(user_id)

        if coins is None:
            await ctx.send("❌ ┃ **Oops! You don’t have an account.** Try `poo start` to create one!")
            return

        if coins <= 0:
            await ctx.send(f"💸 ┃ **{name}**, you poor thing! You do not have enough **Crap Cash**.")
            return

        if amount.lower() == "all":
            bet = min(coins, MAX_BET)
        else:
            try:
                bet = int(amount)
            except ValueError:
                await ctx.send("❌ ┃ Oops! That’s not it! Enter a valid number!")
                return

        if bet <= 0:
            await ctx.send("❌ ┃ Oops! Bet must be above **0 Crap Cash**.")
            return

        if bet > MAX_BET:
            await ctx.send(f"⚠️ ┃ Easy! Maximum bet is **{MAX_BET:,} Crap Cash**.")
            return

        if bet > coins:
            await ctx.send(f"💸 ┃ **{name}**, you need **{bet:,} Crap Cash** but only have **{coins:,}**.")
            return

        await self.remove_coins(user_id, bet)

        deck = ["A♠","2♠","3♠","4♠","5♠","6♠","7♠","8♠","9♠","10♠","J♠","Q♠","K♠"] * 4
        random.shuffle(deck)

        values = {
            "A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
            "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10
        }

        def hand_value(cards):
            total = sum(values[card[:-1]] for card in cards)
            aces = sum(1 for card in cards if card[:-1] == "A")
            while total > 21 and aces:
                total -= 10
                aces -= 1
            return total

        def cards_text(cards):
            return " ".join(cards)

        def draw_card():
            return deck.pop()

        player_cards = [draw_card(), draw_card()]
        dealer_cards = [draw_card(), draw_card()]

        # Natural Blackjack check
        if hand_value(player_cards) == 21:
            reward = bet * 3
            await self.add_coins(user_id, reward)
            embed = discord.Embed(
                title="🃏✨ ┃ Natural Blackjack!",
                description=(
                    f"🃏 ┃ Your Cards:\n`{cards_text(player_cards)}`\nTotal : **21**\n\n"
                    f"🎉 ┃ **{name} won {reward:,} Crap Cash!**"
                ),
                color=Colors.SUCCESS
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="🃏 ┃ Blackjack",
            description=(
                f"**{name}** bet **{bet:,} Crap Cash**\n\n"
                f"🃏 ┃ Your Cards :\n`{cards_text(player_cards)}`\n"
                f"Total : **{hand_value(player_cards)}**\n\n"
                f"🎴 ┃ Dealer :\n`{dealer_cards[0]} ❓`"
            ),
            color=Colors.WARNING
        )

        view = BlackjackView(user_id)
        message = await ctx.send(embed=embed, view=view)
        view.message = message

        while True:
            timeout = await view.wait()

            if timeout or view.choice is None:
                embed = discord.Embed(
                    title="⏰ ┃ Blackjack Timeout",
                    description=f"**{name}** took too long.\n\nLost **{bet:,} Crap Cash.**",
                    color=Colors.ERROR
                )
                await message.edit(embed=embed, view=None)
                return

            if view.choice == "hit":
                player_cards.append(draw_card())
                player_total = hand_value(player_cards)

                if player_total > 21:
                    embed = discord.Embed(
                        title="💀 ┃ Blackjack Bust",
                        description=(
                            f"🃏 ┃ Your Cards :\n`{cards_text(player_cards)}`\n"
                            f"Total : **{player_total}**\n\n"
                            f"💀 ┃ **{name} lost {bet:,} Crap Cash.**"
                        ),
                        color=Colors.ERROR
                    )
                    await message.edit(embed=embed, view=None)
                    return

                view = BlackjackView(user_id)
                embed.description = (
                    f"**{name}** bet **{bet:,} Crap Cash**\n\n"
                    f"🃏 ┃ Your Cards :\n`{cards_text(player_cards)}`\n"
                    f"Total : **{player_total}**\n\n"
                    f"🎴 ┃ Dealer :\n`{dealer_cards[0]} ❓`"
                )
                message = await message.edit(embed=embed, view=view)
                view.message = message

            elif view.choice == "stand":
                break

        # Dealer turn
        while hand_value(dealer_cards) < 17:
            dealer_cards.append(draw_card())

        player_total = hand_value(player_cards)
        dealer_total = hand_value(dealer_cards)

        if dealer_total > 21:
            reward = bet * 2
            await self.add_coins(user_id, reward)
            title, color = "🎉 ┃ Blackjack Win", Colors.SUCCESS
            result = f"Dealer busted! **{name} won {reward:,} Crap Cash!**"

        elif player_total > dealer_total:
            reward = bet * 2
            await self.add_coins(user_id, reward)
            title, color = "🎉 ┃ Blackjack Win", Colors.SUCCESS
            result = f"**{name} won {reward:,} Crap Cash!**"

        elif player_total == dealer_total:
            await self.add_coins(user_id, bet)
            title, color = "🤝 ┃ Blackjack Draw", Colors.WARNING
            result = f"**{name}**, your bet was returned."

        else:
            title, color = "💀 ┃ Blackjack Lose", Colors.ERROR
            result = f"**{name} lost {bet:,} Crap Cash.**"

        embed = discord.Embed(
            title=title,
            description=(
                f"🃏 ┃ Your Cards :\n`{cards_text(player_cards)}`\n"
                f"Total : **{player_total}**\n\n"
                f"🎴 ┃ Dealer Cards :\n`{cards_text(dealer_cards)}`\n"
                f"Total : **{dealer_total}**\n\n"
                f"{result}"
            ),
            color=color
        )
        await message.edit(embed=embed, view=None)


async def setup(bot):
    await bot.add_cog(Casino(bot))