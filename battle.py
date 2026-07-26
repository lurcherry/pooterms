import discord
import random
import asyncio
import aiosqlite

from datetime import datetime, timedelta

from discord.ext import commands
from discord.ui import View

from utils.items import get_item
from utils.colors import Colors
from utils.rank import add_star, remove_star
from utils.inventory import add_inventory_item


DB_PATH = "data/database.db"


pending_battles = {}
active_battles = {}
battle_timers = {}



class BattleView(View):

    def __init__(
        self,
        cog,
        battle_id
    ):

        super().__init__(
            timeout=None
        )

        self.cog = cog
        self.battle_id = battle_id



    @discord.ui.button(
        label="Attack",
        emoji="⚔️",
        style=discord.ButtonStyle.danger,
        custom_id="poo_battle_attack"
    )
    async def attack(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.defer()

        await self.cog.attack_turn(
            interaction,
            self.battle_id
        )



    @discord.ui.button(
        label="Surrender",
        emoji="🏳️",
        style=discord.ButtonStyle.secondary,
        custom_id="poo_battle_surrender"
    )
    async def surrender(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await self.cog.surrender(
            interaction,
            self.battle_id
        )




class Battle(commands.Cog):

    def __init__(
        self,
        bot
    ):

        self.bot = bot
    async def get_player_hp(
        self,
        user_id
    ):

        async with aiosqlite.connect(
            DB_PATH
        ) as db:

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

            result = await cursor.fetchone()


        if result is None:

            return 100


        return result[0]




    async def update_player_hp(
        self,
        user_id,
        hp
    ):

        if hp < 0:

            hp = 0


        if hp > 100:

            hp = 100



        async with aiosqlite.connect(
            DB_PATH
        ) as db:

            await db.execute(
                """
                UPDATE players
                SET hp = ?
                WHERE user_id = ?
                """,
                (
                    hp,
                    user_id
                )
            )

            await db.commit()




    async def set_battle_cooldown(
        self,
        user_id,
        minutes
    ):

        cooldown = datetime.now() + timedelta(
            minutes=minutes
        )


        async with aiosqlite.connect(
            DB_PATH
        ) as db:

            await db.execute(
                """
                UPDATE players
                SET battle_cooldown = ?
                WHERE user_id = ?
                """,
                (
                    cooldown.isoformat(),
                    user_id
                )
            )

            await db.commit()




    async def get_battle_cooldown(
        self,
        user_id
    ):

        async with aiosqlite.connect(
            DB_PATH
        ) as db:

            cursor = await db.execute(
                """
                SELECT battle_cooldown
                FROM players
                WHERE user_id = ?
                """,
                (
                    user_id,
                )
            )

            result = await cursor.fetchone()



        if result is None:

            return None



        return result[0]




    async def update_level(
        self,
        user_id
    ):

        async with aiosqlite.connect(
            DB_PATH
        ) as db:

            cursor = await db.execute(
                """
                SELECT level, experience
                FROM players
                WHERE user_id = ?
                """,
                (
                    user_id,
                )
            )

            data = await cursor.fetchone()



        if data is None:

            return



        level, exp = data


        required = level * 100



        while exp >= required:

            exp -= required

            level += 1

            required = level * 100




        async with aiosqlite.connect(
            DB_PATH
        ) as db:

            await db.execute(
                """
                UPDATE players
                SET
                    level = ?,
                    experience = ?
                WHERE user_id = ?
                """,
                (
                    level,
                    exp,
                    user_id
                )
            )

            await db.commit()




    async def update_rank(
        self,
        user_id
    ):

        async with aiosqlite.connect(
            DB_PATH
        ) as db:

            cursor = await db.execute(
                """
                SELECT rank, stars
                FROM players
                WHERE user_id = ?
                """,
                (
                    user_id,
                )
            )

            data = await cursor.fetchone()



        if data is None:

            return None



        rank, stars = data



        result = add_star(
            rank,
            stars
        )



        rank, stars, promoted, old_rank = result



        async with aiosqlite.connect(
            DB_PATH
        ) as db:

            await db.execute(
                """
                UPDATE players
                SET
                    rank = ?,
                    stars = ?
                WHERE user_id = ?
                """,
                (
                    rank,
                    stars,
                    user_id
                )
            )

            await db.commit()



        return {

            "promoted": promoted,

            "old_rank": old_rank,

            "new_rank": rank

        }




    async def update_rank_loss(
        self,
        user_id
    ):

        async with aiosqlite.connect(
            DB_PATH
        ) as db:

            cursor = await db.execute(
                """
                SELECT rank, stars
                FROM players
                WHERE user_id = ?
                """,
                (
                    user_id,
                )
            )

            data = await cursor.fetchone()



        if data is None:

            return None



        rank, stars = data



        result = remove_star(
            rank,
            stars
        )



        if len(result) == 4:

            rank, stars, demoted, old_rank = result

        else:

            rank, stars = result

            demoted = False

            old_rank = rank




        async with aiosqlite.connect(
            DB_PATH
        ) as db:

            await db.execute(
                """
                UPDATE players
                SET
                    rank = ?,
                    stars = ?,
                    battle_result = 'down'
                WHERE user_id = ?
                """,
                (
                    rank,
                    stars,
                    user_id
                )
            )

            await db.commit()



        return {

            "demoted": demoted,

            "old_rank": old_rank,

            "new_rank": rank,

            "stars": stars

        }

    
    async def get_combat_stats(
        self,
        user_id
    ):

        async with aiosqlite.connect(
            DB_PATH
        ) as db:

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
                    user_id,
                )
            )

            equipment = await cursor.fetchone()



        attack = 5
        defense = 0


        weapon = "No weapon equipped."
        armor = "No armor equipped."



        if equipment:

            if (
                equipment[0]
                and equipment[0] != "None"
                and equipment[2] > 0
            ):

                weapon = equipment[0]


                item = get_item(
                    weapon
                )


                if item:

                    attack += item.get(
                        "attack",
                        0
                    )



            if (
                equipment[1]
                and equipment[1] != "None"
                and equipment[3] > 0
            ):


                armor = equipment[1]


                item = get_item(
                    armor
                )


                if item:

                    defense += item.get(
                        "defense",
                        0
                    )



        return {

            "attack": attack,

            "defense": defense,

            "weapon": weapon,

            "armor": armor,

            "weapon_durability": equipment[2] if equipment else 0,

            "armor_durability": equipment[3] if equipment else 0

        }


    async def reduce_durability(
        self,
        user_id,
        weapon=False,
        armor=False
    ):

        async with aiosqlite.connect(
            DB_PATH
        ) as db:

            if weapon:

                await db.execute(
                    """
                    UPDATE equipment
                    SET weapon_durability =
                        CASE
                            WHEN weapon_durability > 0
                            THEN weapon_durability - 1
                            ELSE 0
                        END
                    WHERE user_id = ?
                    """,
                    (
                        user_id,
                    )
                )


            if armor:

                await db.execute(
                    """
                    UPDATE equipment
                    SET armor_durability =
                        CASE
                            WHEN armor_durability > 0
                            THEN armor_durability - 1
                            ELSE 0
                        END
                    WHERE user_id = ?
                    """,
                    (
                        user_id,
                    )
                )


            await db.commit()



    async def get_player_info(
        self,
        user_id
    ):

        async with aiosqlite.connect(
            DB_PATH
        ) as db:

            cursor = await db.execute(
                """
                SELECT
                    level,
                    rank,
                    stars
                FROM players
                WHERE user_id = ?
                """,
                (
                    user_id,
                )
            )


            data = await cursor.fetchone()



        if data is None:

            return {

                "level": 1,

                "rank": "Unranked",

                "stars": 0

            }



        return {

            "level": data[0],

            "rank": data[1],

            "stars": data[2]

        }






    async def build_embed(
        self,
        battle
    ):

        embed = discord.Embed(

            title="⚔️ ┃ POO Battle",

            color=discord.Color.red()

        )



        for player in battle["players"]:


            hp = battle["hp"].get(
                player,
                100
            )



            filled = int(
                hp / 10
            )



            if filled < 0:

                filled = 0



            if filled > 10:

                filled = 10



            bar = (

                "🟥" * filled

                +

                "⬜" * (10 - filled)

            )



            combat = await self.get_combat_stats(
                player
            )



            info = await self.get_player_info(
                player
            )



            stars = (

                "⭐" * info["stars"]

                +

                "☆" * (5 - info["stars"])

            )



            embed.add_field(

                name=f"👤 ┃ {battle['names'][player]}",

                value=(

                    "❤️ ┃ HP\n"

                    f"{bar}\n"

                    f"**{hp}/100**\n\n"


                    f"⚔️ ┃ Weapon : **{combat['weapon']}**\n"
                    f"🔧 ┃ Durability : **{combat['weapon_durability']}/100**\n\n"

                    f"🛡️ ┃ Armor : **{combat['armor']}**\n"
                    f"🔧 ┃ Durability : **{combat['armor_durability']}/100**\n\n"


                    f"📈 ┃ Level : **{info['level']}**\n"
                    f"⭐ ┃ Rank : **{info['rank']} {stars}**"

                ),

                inline=False

            )

        return embed



    @commands.command()
    async def battle(
        self,
        ctx,
        member: discord.Member = None
    ):

        user_id = ctx.author.id



        cooldown = await self.get_battle_cooldown(
            user_id
        )



        if cooldown:

            cooldown_time = datetime.fromisoformat(
                cooldown
            )


            if datetime.now() < cooldown_time:


                remaining = (
                    cooldown_time - datetime.now()
                )


                await ctx.send(

                    f"⏳ ┃ You are on battle cooldown.\n"
                    f"Try again in **{int(remaining.total_seconds())} seconds**."

                )

                return




        if member is None:


            await ctx.send(

                "⚔️ ┃ Mention someone to battle."

            )

            return




        if member.bot:


            await ctx.send(

                "❌ ┃ You cannot battle bots."

            )

            return




        if member == ctx.author:


            await ctx.send(

                "❌ ┃ You cannot battle yourself."

            )

            return




        async with aiosqlite.connect(
            DB_PATH
        ) as db:


            cursor = await db.execute(

                """
                SELECT user_id
                FROM players
                WHERE user_id = ?
                """,

                (
                    member.id,
                )

            )


            opponent = await cursor.fetchone()


        opponent_cooldown = await self.get_battle_cooldown(
            member.id
        )

        if opponent_cooldown:

            cooldown_time = datetime.fromisoformat(
                opponent_cooldown
            )

            if datetime.now() < cooldown_time:

                remaining = (
                    cooldown_time - datetime.now()
                )

                await ctx.send(

                    f"⏳ ┃ Uh oh! {member.mention} is on battle cooldown.\n"
                    f"Try again in **{int(remaining.total_seconds())} seconds**."

                )

                return



        if opponent is None:


            await ctx.send(

                f"❌ ┃ {member.mention} does not have a POO account."

            )

            return





        if ctx.author.id in pending_battles:


            await ctx.send(

                "❌ ┃ You already have a pending battle."

            )

            return




        if member.id in pending_battles:


            await ctx.send(

                "❌ ┃ That player already has a pending battle."

            )

            return





        pending_battles[member.id] = {


            "challenger": ctx.author.id,


            "channel": ctx.channel.id


        }




        await ctx.send(

            f"⚔️ ┃ {ctx.author.mention} challenged "
            f"{member.mention}!\n\n"

            "✅ ┃ Type `poo accept`\n"
            "❌ ┃ Type `poo decline`\n\n"

            "⌛ ┃ Expires in **60 seconds**."

        )




        await asyncio.sleep(
            60
        )




        if member.id in pending_battles:


            del pending_battles[member.id]



            await ctx.send(

                "⌛ ┃ Battle request expired."

            )

    @commands.command()
    async def accept(
        self,
        ctx
    ):

        request = pending_battles.get(
            ctx.author.id
        )


        if request is None:


            await ctx.send(

                "❌ ┃ Nobody challenged you."

            )

            return




        del pending_battles[ctx.author.id]



        challenger_id = request["challenger"]



        players = [

            challenger_id,

            ctx.author.id

        ]




        first_turn = random.choice(
            players
        )




        battle_id = random.randint(
            100000,
            999999
        )




        challenger_user = await self.bot.fetch_user(
            players[0]
        )


        opponent_user = await self.bot.fetch_user(
            players[1]
        )




        player_one_hp = await self.get_player_hp(
            players[0]
        )


        player_two_hp = await self.get_player_hp(
            players[1]
        )

        if player_one_hp <= 0:

            await ctx.send(
                f"❌ ┃ <@{players[0]}> has 0 HP and cannot battle."
            )

            return


        if player_two_hp <= 0:

            await ctx.send(
                f"❌ ┃ <@{players[1]}> has 0 HP and cannot battle."
            )

            return





        active_battles[battle_id] = {
            


            "players": players,


            "turn": first_turn,


            "message": None,


            "log_message": None,


            "channel": ctx.channel.id,


            "last_action": asyncio.get_event_loop().time(),



            "names": {


                players[0]: challenger_user.display_name,


                players[1]: opponent_user.display_name


            },



            "hp": {


                players[0]: player_one_hp,


                players[1]: player_two_hp


            },



            "log": (

                f"🎲 <@{first_turn}> attacks first."

            )


        }






        battle = active_battles[battle_id]





        await ctx.send(

            f"✅ ┃ {ctx.author.mention} accepted the battle!\n"

            f"⚔️ ┃ Battle starting...\n\n"

            f"<@{players[0]}> vs <@{players[1]}>"

        )




        message = await ctx.send(

            embed=await self.build_embed(
                battle
            ),


            view=BattleView(

                self,

                battle_id

            )

        )

        battle["message"] = message

        log_message = await ctx.send(
            f"🎲 ┃ <@{first_turn}> attacks first."
        )

        battle["log_message"] = log_message





        battle_timers[battle_id] = asyncio.create_task(

            self.start_afk_timer(

                battle_id

            )
        )

    async def attack_turn(
        self,
        interaction,
        battle_id
    ):


        battle = active_battles.get(
            battle_id
        )


        if battle is None:


            await interaction.followup.send(

                "❌ ┃ Battle ended.",

                ephemeral=True

            )

            return




        user_id = interaction.user.id




        if user_id != battle["turn"]:


            await interaction.followup.send(

                "❌ ┃ It is not your turn.",

                ephemeral=True

            )

            return





        opponent = next(

            player for player in battle["players"]

            if player != user_id

        )





        attacker_stats = await self.get_combat_stats(
            user_id
        )


        defender_stats = await self.get_combat_stats(
            opponent
        )





        damage = random.randint(
            5,
            10
        )



        damage += attacker_stats["attack"]




        damage -= defender_stats["defense"]




        if damage < 1:

            damage = 1





        new_hp = battle["hp"][opponent] - damage





        if new_hp < 0:

            new_hp = 0





        battle["hp"][opponent] = new_hp




        await self.update_player_hp(

            opponent,

            new_hp

        )

        await self.reduce_durability(
            user_id,
            weapon=True
        )

        await self.reduce_durability(
            opponent,
            armor=True
        )





        if new_hp <= 0:



            rewards = await self.give_rewards(

                user_id,

                opponent

            )




            await self.set_battle_cooldown(

                user_id,

                1

            )


            await self.set_battle_cooldown(

                opponent,

                1

            )




            await battle["log_message"].edit(
                content=(
                    f"🏆 ┃ Yey! <@{user_id}> won the battle!\n"
                    f"💀 ┃ <@{opponent}> has been defeated. How unfortunate."
                )
            )



            await interaction.edit_original_response(

                embed=await self.build_embed(
                    battle
                ),

                view=None

            )





            await interaction.followup.send(

                embed=await self.winner_reward_embed(

                    user_id,

                    rewards
                )
            )

            await interaction.followup.send(

                embed=await self.loser_reward_embed(

                    opponent,

                    rewards
                )
            )

            if battle_id in battle_timers:

                battle_timers[battle_id].cancel()

                del battle_timers[battle_id]

            del active_battles[battle_id]


            return







        battle["turn"] = opponent




        battle["last_action"] = asyncio.get_event_loop().time()





        channel = self.bot.get_channel(battle["channel"])

        if channel:

            await battle["log_message"].edit(

                content=(

                    f"⚔️ ┃ <@{user_id}> attacked!\n"

                    f"💥 ┃ Damage dealt : **{damage}**\n"

                    f"⏳ ┃ Waiting for <@{opponent}>."

                )

            )






        await interaction.edit_original_response(

            embed=await self.build_embed(

            battle

        ),

        view=BattleView(

            self,

            battle_id

        )

    )

    @commands.command()
    async def decline(
        self,
        ctx
    ):


        request = pending_battles.get(
            ctx.author.id
        )



        if request is None:


            await ctx.send(

                "❌ ┃ Nobody challenged you."

            )

            return





        challenger = request["challenger"]





        del pending_battles[ctx.author.id]






        await ctx.send(

            f"❌ ┃ {ctx.author.mention} declined "
            f"<@{challenger}>'s battle."

        )








    async def start_afk_timer(
        self,
        battle_id
    ):



        await asyncio.sleep(
            300
        )




        battle = active_battles.get(
            battle_id
        )




        if battle is None:


            return





        loser = battle["turn"]





        winner = next(

            player for player in battle["players"]

            if player != loser

        )






        rank_result = await self.update_rank_loss(

            loser
        )

        rewards = await self.give_rewards(

            winner,

            loser
        )




        await self.set_battle_cooldown(

            winner,

            1

        )




        await self.set_battle_cooldown(

            loser,

            5

        )






        await battle["log_message"].edit(

            content=(

                f"⏰ ┃ Left us hanging... <@{loser}> was inactive for 5 minutes!\n"

                f"🏆 ┃ So, <@{winner}> wins the battle!"
            )
        )







        # send final result if message still exists

        channel = self.bot.get_channel(

            battle.get("channel")

        )





        if channel:

            if battle.get("message"):

                await battle["message"].edit(
                    view=None
                )

            await channel.send(

                embed=await self.build_embed(

                    battle

                )

            )



            await channel.send(

                embed=await self.winner_reward_embed(

                    winner,

                    rewards
                )
            )


            await channel.send(

                embed=await self.loser_reward_embed(

                    loser,

                    rewards,

                    rank_result
                )
            )

            


        if battle_id in battle_timers:
            del battle_timers[battle_id]


        del active_battles[battle_id]


    async def surrender(
        self,
        interaction,
        battle_id
    ):


        battle = active_battles.get(
            battle_id
        )



        if battle is None:


            await interaction.response.send_message(

                "❌ ┃ Battle ended.",

                ephemeral=True

            )

            return






        loser = interaction.user.id




        if loser not in battle["players"]:


            await interaction.response.send_message(

                "❌ ┃ You are not in this battle.",

                ephemeral=True

            )

            return






        winner = next(

            player for player in battle["players"]

            if player != loser

        )






        rewards = await self.give_rewards(

            winner,

            loser

        )





        rank_result = await self.update_rank_loss(

            loser

        )

        winner_rank_result = await self.update_rank(

            winner

        )




        await self.set_battle_cooldown(

            winner,

            1

        )



        await self.set_battle_cooldown(

            loser,

            5

        )







        await battle["log_message"].edit(

            content=(

                f"🏳️ ┃ Oh dang... <@{loser}> surrendered!\n"
                f"🏆 ┃ Well, <@{winner}> wins the battle!"

            )

        )







        await interaction.response.edit_message(

            embed=await self.build_embed(

                battle

            ),

            view=None

        )



        if winner_rank_result and winner_rank_result["promoted"]:

            rewards["rank_result"] = {

                "promoted": True,

                "demoted": False,

                "old_rank": winner_rank_result["old_rank"],

                "new_rank": winner_rank_result["new_rank"]

            }


        elif rank_result and rank_result["demoted"]:

            rewards["rank_result"] = {

                "promoted": False,

                "demoted": True,

                "old_rank": rank_result["old_rank"],

                "new_rank": rank_result["new_rank"]

            }




        await interaction.followup.send(

            embed=await self.winner_reward_embed(

                winner,

                rewards
            )
        )

        await interaction.followup.send(

            embed=await self.loser_reward_embed(

                loser,

                rewards,

                rank_result
            )
        )

        if battle_id in battle_timers:

            battle_timers[battle_id].cancel()

            del battle_timers[battle_id]

        del active_battles[battle_id]



    def roll_lootbox(
        self
    ):

        roll = random.randint(
            1,
            100
        )

        if roll <= 60:

            return "Lucky Lootbox"

        elif roll <= 85:

            return "Fortune Lootbox"

        elif roll <= 97:

            return "Mythic Lootbox"

        else:

            return "Divine Lootbox"

    async def give_rewards(
        self,
        winner_id,
        loser_id
    ):

        winner_exp = random.randint(
            60,
            100
        )

        winner_cash = random.randint(
            250,
            500
        )

        loser_exp = random.randint(
            20,
            50
        )

        loser_cash = random.randint(
            75,
            150
        )

        lootbox = self.roll_lootbox()

        rank_result = await self.update_rank(
            winner_id
        )

        async with aiosqlite.connect(
            DB_PATH
        ) as db:

            await db.execute(
                """
                UPDATE players
                SET
                    experience = experience + ?,
                    coins = coins + ?,
                    wins = wins + 1,
                    battle_result = 'up'
                WHERE user_id = ?
                """,
                (
                    winner_exp,
                    winner_cash,
                    winner_id
                )
            )

            await db.execute(
                """
                UPDATE players
                SET
                    experience = experience + ?,
                    coins = coins + ?,
                    losses = losses + 1
                WHERE user_id = ?
                """,
                (
                    loser_exp,
                    loser_cash,
                    loser_id
                )
            )

            await db.commit()

        await add_inventory_item(
            winner_id,
            lootbox
        )

        await self.update_level(
            winner_id
        )

        await self.update_level(
            loser_id
        )

        winner_info = await self.get_player_info(
            winner_id
        )

        loser_info = await self.get_player_info(
            loser_id
        )

        return {

            "winner_exp": winner_exp,

            "winner_cash": winner_cash,

            "loser_exp": loser_exp,

            "loser_cash": loser_cash,

            "lootbox": lootbox,

            "rank_result": rank_result,

            "winner_rank": winner_info["rank"],

            "winner_stars": winner_info["stars"],

            "loser_rank": loser_info["rank"],

            "loser_stars": loser_info["stars"]

        }

    async def winner_reward_embed(
        self,
        winner_id,
        rewards
    ):

        user = await self.bot.fetch_user(
            winner_id
        )

        embed = discord.Embed(

            title="🏆 ┃ Battle Rewards",

            description=(

                f"Congratulations, **{user.display_name}**!\n\n"

                "You defeated your opponent and survived another messy battle!"

            ),

            color=Colors.SUCCESS

        )

        embed.add_field(

            name=" ",

            value=(

                f"⚡ ┃ EXP : **+{rewards['winner_exp']}**\n"

                f"💰 ┃ Crap Cash : **+{rewards['winner_cash']}**\n"

                f"📦 ┃ Lootbox : **{rewards['lootbox']}**"

            ),

            inline=False

        )

        stars = (
            "⭐" * rewards["winner_stars"] +
            "☆" * (5 - rewards["winner_stars"])
        )

        rank = rewards.get("rank_result")

        if rank and rank["promoted"]:

            rank_progress = (
                f"{rewards['winner_rank']} **{stars}**\n\n"
                f"📈 ┃ Rank Up!\n"
                f"**{rank['old_rank']}** ➜ **{rank['new_rank']}**"
            )

        else:

            rank_progress = (
                f"{rewards['winner_rank']} **{stars}** (+1)"
            )

        embed.add_field(

            name="🏅 ┃ Rank Progress",

            value=rank_progress,

            inline=False

        )

        return embed

    async def loser_reward_embed(
        self,
        loser_id,
        rewards,
        rank_result=None
    ):

        user = await self.bot.fetch_user(
            loser_id
        )

        embed = discord.Embed(

            title="💀 ┃ Better Luck Next Time",

            description=(

                f"Don’t worry, **{user.display_name}**.\n\n"

                "Every defeat is another step toward becoming stronger."

            ),

            color=Colors.ERROR

        )

        embed.add_field(

            name=" ",

            value=(

                f"⚡ ┃ EXP : **+{rewards['loser_exp']}**\n"

                f"💰 ┃ Crap Cash : **+{rewards['loser_cash']}**"

            ),

            inline=False

        )

        star_count = (
            rank_result["stars"]
            if rank_result
            else rewards["loser_stars"]
        )

        stars = (
            "⭐" * star_count +
            "☆" * (5 - star_count)
        )

        rank_progress = (
            f"{rewards['loser_rank']} **{stars}**"
        )

        if rank_result:

            if rank_result.get("demoted"):

                rank_progress = (
                    f"{rank_result['new_rank']} **{stars}** (-1)\n\n"
                    f"📉 ┃ Rank Down!\n"
                    f"**{rank_result['old_rank']}** ➜ **{rank_result['new_rank']}**"
                )

            else:

                rank_progress = (
                    f"{rewards['loser_rank']} **{stars}** (-1)"
                )

        embed.add_field(

            name="📉 ┃ Rank Progress",

            value=rank_progress,

            inline=False

        )

        return embed

async def setup(
    bot
):

    await bot.add_cog(
        Battle(bot)
    )
