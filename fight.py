import discord
import random
import aiosqlite
import time

from discord.ext import commands

from utils.colors import Colors
from utils.monsters import MONSTERS
from utils.lootboxes import roll_drop
from utils.items import get_item
from utils.leveling import calculate_level


DB_PATH = "data/database.db"



async def reduce_weapon_durability(user_id):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT weapon,
                   weapon_durability

            FROM equipment

            WHERE user_id = ?
            """,
            (
                user_id,
            )
        )

        data = await cursor.fetchone()


        if not data or not data[0]:

            return None


        weapon = data[0]

        durability = data[1] or 0

        durability -= 1


        if durability <= 0:

            await db.execute(
                """
                UPDATE equipment

                SET weapon = NULL,
                    weapon_durability = 0

                WHERE user_id = ?
                """,
                (
                    user_id,
                )
            )

            await db.commit()

            return weapon



        await db.execute(
            """
            UPDATE equipment

            SET weapon_durability = ?

            WHERE user_id = ?
            """,
            (
                durability,
                user_id
            )
        )

        await db.commit()


    return None





async def reduce_armor_durability(user_id):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT armor,
                   armor_durability

            FROM equipment

            WHERE user_id = ?
            """,
            (
                user_id,
            )
        )


        data = await cursor.fetchone()


        if not data or not data[0]:

            return None


        armor = data[0]

        durability = data[1] or 0

        durability -= 1



        if durability <= 0:


            await db.execute(
                """
                UPDATE equipment

                SET armor = NULL,
                    armor_durability = 0

                WHERE user_id = ?
                """,
                (
                    user_id,
                )
            )


            await db.commit()

            return armor



        await db.execute(
            """
            UPDATE equipment

            SET armor_durability = ?

            WHERE user_id = ?
            """,
            (
                durability,
                user_id
            )
        )


        await db.commit()


    return None




active_fights = {}

fight_cooldowns = {}


class Fight(commands.Cog):


    def __init__(self, bot):

        self.bot = bot




    @commands.command()
    async def fight(self, ctx):

        user_id = ctx.author.id

        name = ctx.author.display_name

        if user_id in fight_cooldowns:

            remaining = fight_cooldowns[user_id] - time.time()
            
            if remaining > 0:
                await ctx.send(
                f"⏳ ┃ **{name}**, wait **{int(remaining)}s** before fighting again."
            )
                
                return

        if user_id in active_fights:

            await ctx.send(
                f"⚔️ ┃ **{name}**, you are already fighting!"
            )

            return




        async with aiosqlite.connect(DB_PATH) as db:

            cursor = await db.execute(
                """
                SELECT hp

                FROM players

                WHERE user_id = ?
                """,
                (
                    user_id,
                )
            )


            player = await cursor.fetchone()




        if player is None:

            await ctx.send(
                f"**{name}**, create your account first with `poo start`."
            )

            return



        monster_pool = []


        for monster_name, monster_data in MONSTERS.items():


            rarity = monster_data.get(
                "rarity",
                "⚪ Common"
            )


            if rarity == "⚪ Common":

                chance = 60


            elif rarity == "🟢 Uncommon":

                chance = 25


            elif rarity == "🔵 Rare":

                chance = 10


            elif rarity == "🟣 Epic":

                chance = 4


            elif rarity == "🟡 Legendary":

                chance = 1


            else:

                chance = 10



            monster_pool.extend(
                [monster_name] * chance
            )



        monster_name = random.choice(
            monster_pool
        )


        monster = MONSTERS[monster_name]



        active_fights[user_id] = {

            "monster": monster_name,

            "monster_hp": monster["hp"],

            "monster_max_hp": monster["hp"],

            "player_hp": player[0],
            "player_max_hp": 100

        }




        embed = discord.Embed(

            title=f"{monster['emoji']} A Wild {monster_name} Appeared!",

            description=(

                f"👾 ┃ **{monster_name}**\n"

                f"✨ ┃ Rarity : **{monster['rarity']}**\n"

                f"❤️ ┃ HP : **{monster['hp']}/{monster['hp']}**\n\n"


                f"**{name}**\n"

                f"❤️ ┃ HP : **{player[0]}/100**\n\n"


                "Choose your action!"

            ),

            color=Colors.ERROR

        )



        view = FightButtons(
            user_id
        )


        message = await ctx.send(

            embed=embed,

            view=view

        )


        view.message = message



class FightButtons(discord.ui.View):

    def set_cooldown(self, seconds):
        fight_cooldowns[self.user_id] = time.time() + seconds


    def __init__(self, user_id):

        super().__init__(
            timeout=60
        )

        self.user_id = user_id

        self.message = None

        self.ended = False


    async def interaction_check(self, interaction):


        if interaction.user.id != self.user_id:


            await interaction.response.send_message(

                "❌ ┃ This battle is not yours, silly.",

                ephemeral=True

            )

            return False



        return True






    @discord.ui.button(

        label="Strike",

        emoji="⚔️",

        style=discord.ButtonStyle.danger

    )
    async def strike(

        self,

        interaction,

        button

    ):


        await interaction.response.defer()



        battle = active_fights.get(
            self.user_id
        )



        if battle is None:


            await interaction.followup.send(

                "❌ ┃ This battle already ended.",

                ephemeral=True

            )

            return




        monster = MONSTERS[

            battle["monster"]

        ]






        player_damage = random.randint(

            10,

            25

        )


        broken_weapon = None




        async with aiosqlite.connect(DB_PATH) as db:


            cursor = await db.execute(

                """
                SELECT weapon

                FROM equipment

                WHERE user_id = ?
                """,

                (
                    self.user_id,
                )

            )


            weapon_data = await cursor.fetchone()





        if weapon_data and weapon_data[0]:


            weapon = get_item(

                weapon_data[0]

            )


            if weapon:


                player_damage += weapon.get(

                    "attack",

                    0

                )


                broken_weapon = await reduce_weapon_durability(

                    self.user_id

                )




        battle["monster_hp"] -= player_damage
        if battle["monster_hp"] < 0:
            battle["monster_hp"] = 0
        if battle["monster_hp"] <= 0:
            await self.victory(
                 interaction,
                 battle,
                 monster,
                 player_damage,
                 broken_weapon
                   )
            return




        monster_damage = random.randint(
            5,
            monster["attack"]
        )


        armor_defense = 0

        broken_armor = None



        async with aiosqlite.connect(DB_PATH) as db:

            cursor = await db.execute(
                """
                SELECT armor

                FROM equipment

                WHERE user_id = ?
                """,
                (
                    self.user_id,
                )
            )


            armor_data = await cursor.fetchone()

            if armor_data and armor_data[0]:

                armor = get_item(
                    armor_data[0]
                )

                if armor:

                    armor_defense = armor.get(
                        "defense",
                        0
                    )

                    broken_armor = await reduce_armor_durability(
                        self.user_id
                    )


            monster_damage -= armor_defense

            if monster_damage < 0:
                monster_damage = 0


            battle["player_hp"] -= monster_damage


                
            async with aiosqlite.connect(DB_PATH) as db:
                    
                await db.execute(
                    """
                    UPDATE players
                    SET hp = ?
                    WHERE user_id = ?
                    """,
                        (
                            battle["player_hp"],
                            self.user_id
                                )
                                    )
                await db.commit()


        if battle["player_hp"] <= 0:


            async with aiosqlite.connect(DB_PATH) as db:


                await db.execute(
                    """
                    UPDATE players

                    SET hp = 100,
                        losses = losses + 1

                    WHERE user_id = ?
                    """,
                    (
                        self.user_id,
                    )
                )
                
                await db.commit()


            embed = discord.Embed(

                title="💀 ┃ You Were Defeated",

                description=(

                    f"**{interaction.user.display_name}**, "

                    f"the **{battle['monster']}** defeated you.\n\n"

                    "Train harder and come back stronger!"

                ),

                color=Colors.ERROR

            )



            await interaction.edit_original_response(

                embed=embed,

                view=None

            )


            if self.user_id in active_fights:

                del active_fights[
                    self.user_id
                ]


            return





        broken_text = ""


        if broken_armor:

            broken_text += (

                f"\n💥 ┃ **{broken_armor} broke!**\n"

                "Your armor has been removed."

            )



        if broken_weapon:

            broken_text += (

                f"\n💥 ┃ **{broken_weapon} broke!**\n"

                "Your weapon has been removed."

            )



        embed = discord.Embed(

            title="⚔️ ┃ Battle",

            description=(

                f"**{interaction.user.display_name}**\n\n"


                f"💥 ┃ You dealt **{player_damage} damage**\n\n"


                f"👾 ┃ **{battle['monster']}**\n"

                f"❤️ ┃ HP : **{battle['monster_hp']}/"
                f"{battle['monster_max_hp']}**\n\n"


                f"💔 ┃ Monster attacked!\n"

                f"You received **{monster_damage} damage**\n\n"


                f"❤️ ┃ Your HP : **{battle['player_hp']}/"

                f"{battle['player_max_hp']}**"


                f"{broken_text}"

            ),

            color=Colors.PRIMARY

        )



        await interaction.edit_original_response(
            content=None,

            embed=embed,

            view=self

        )


    async def victory(
        self,
        interaction,
        battle,
        monster,
        damage,
        broken_weapon
    ):

        coins = random.randint(
            monster["coins"][0],
            monster["coins"][1]
        )

        experience = random.randint(
            monster["experience"][0],
            monster["experience"][1]
        )


        drops = roll_drop(
            monster["loot"]
        )


        async with aiosqlite.connect(DB_PATH) as db:

            cursor = await db.execute(
                """
                SELECT experience,
                       level

                FROM players

                WHERE user_id = ?
                """,
                (
                    self.user_id,
                )
            )


            current = await cursor.fetchone()


            old_level = current[1]


            total_exp = current[0] + experience


            new_level, new_exp = calculate_level(
                total_exp
            )


            await db.execute(
                """
                UPDATE players

                SET coins = coins + ?,
                    experience = ?,
                    level = ?,
                    wins = wins + 1

                WHERE user_id = ?
                """,
                (
                    coins,
                    new_exp,
                    new_level,
                    self.user_id
                )
            )
    
            for drop in drops:

                await db.execute(
                    """
                    INSERT INTO inventory
                    (
                        user_id,
                        item_name,
                        amount
                    )
                    VALUES (?, ?, ?)

                    ON CONFLICT(user_id, item_name)

                    DO UPDATE SET amount = amount + excluded.amount
                    """,
                    (
                        self.user_id,
                        drop["item"],
                        drop["amount"]
                    )
                )

            await db.commit()


        loot_text = ""


        if drops:

            loot_text = "\n\n🎁 ┃ **Loot Found :**\n"


            for drop in drops:

                item = get_item(
                    drop["item"]
                )


                if item:

                    loot_text += (
                        f"{item['emoji']} "
                        f"**{drop['item']}** ×{drop['amount']}\n"
                        f"{item['rarity']}\n"
                    )


                else:

                    loot_text += (
                        f"📦 ┃ **{drop['item']}** ×{drop['amount']}\n"
                    )


        else:

            loot_text = (
                "\n\n🎁 ┃ **Loot Found :**\n"
                "Nothing..."
            )


        level_text = ""


        if new_level > old_level:

            level_text = (
                f"\n\n🎉 ┃ **Level Up!**\n"
                f"⭐ ┃ You reached Level **{new_level}**!"
            )


        broken_text = ""


        if broken_weapon:

            broken_text = (
                f"\n\n💥 ┃ **{broken_weapon} broke!**\n"
                "Your weapon has been removed."
            )


        embed = discord.Embed(

            title="👑 ┃ Victory!",

            description=(

                f"**{interaction.user.display_name}** "
                f"defeated **{battle['monster']}**!\n\n"

                f"⚔️ ┃ Damage dealt : **{damage}**\n\n"

                f"💰 ┃ +{coins:,} Crap Cash\n"

                f"⭐ ┃ +{experience} EXP"

                f"{level_text}"

                f"{loot_text}"

                f"{broken_text}"

            ),

            color=Colors.SUCCESS
        )

        self.ended = True

        await interaction.edit_original_response(
            embed=embed,
            view=None
        )


        if self.user_id in active_fights:

            del active_fights[
                self.user_id
            ]
            
        self.set_cooldown(10)
        
        self.stop()

        return


    @discord.ui.button(

        label="Run",

        emoji="🏃🏼‍♂️",

        style=discord.ButtonStyle.secondary

    )
    async def run(

        self,

        interaction,

        button

    ):


        await interaction.response.defer()



        name = interaction.user.display_name



        await interaction.edit_original_response(

            content=(

                f"🏃🏼‍♂️ ┃ **{name}**, you escaped!\n"

                "The monster watched you run away. Your dignity, however, is still being questioned."

            ),

            embed=None,

            view=None

        )



        if self.user_id in active_fights:


            del active_fights[

                self.user_id

            ]
        self.set_cooldown(120)

        self.stop()




    async def on_timeout(self):


        if self.user_id in active_fights:


            del active_fights[

                self.user_id

            ]

        fight_cooldowns[self.user_id] = time.time() + 60




        if self.message:


            await self.message.edit(

                content=(

                    "⏰ ┃ Battle timed out.\n"

                    "The monster got bored and left."

                ),

                embed=None,

                view=None

            )



async def setup(bot):


    await bot.add_cog(

        Fight(bot)

    )