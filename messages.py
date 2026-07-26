class Messages:


    @staticmethod
    def already_registered(name):

        return (

            f"🚫 ┃ **{name}**, easy there!\n\n"

            "You already have an account.\n"
            "No need to make another one."

        )


    @staticmethod
    def account_created(name):

        return (

            f"🎉 Welcome **{name}**!\n\n"

            "Your POO adventure begins now."

        )


    @staticmethod
    def not_registered(name):

        return (

            f"**{name}**, you don’t have an account yet.\n\n"

            "Use `poo start` to create one."

        )




    @staticmethod
    def not_enough_coins(
        name,
        required,
        current
    ):

        return (

            f"**{name}**, you poor thing...\n\n"

            f"You need **{required:,} Crap Cash**, "

            f"but you only have **{current:,}**.\n\n"

            "Go bonk a few monsters with `poo fight` "
            "or test your luck at the casino!"

        )



    @staticmethod
    def daily_cooldown(
        name,
        time
    ):

        return (

            f"**{name}**, whoa, already?\n\n"

            f"Your Daily Loot Box isn’t ready yet.\n"

            f"Come back in **{time}**."

        )




    @staticmethod
    def item_not_found(name):

        return (

            f"**{name}**, you don’t have that item, silly!\n\n"

            "Go bonk a few monsters with `poo fight` first."

        )



    @staticmethod
    def empty_inventory(name):

        return (

            f"**{name}**, it’s... empty.\n\n"

            "Not even a pebble. "
            "Go hunting with `poo fight`!"

        )




    @staticmethod
    def cannot_equip(name):

        return (

            f"**{name}**, you can’t equip something you don’t own.\n\n"

            "Monsters aren’t going to drop themselves.\n"

            "Try `poo fight`."

        )



    @staticmethod
    def already_equipped(name):

        return (

            f"**{name}**, you’re already holding that weapon!\n\n"

            "One sword is enough... "
            "unless you grow another arm."

        )



    @staticmethod
    def unequip(name, item):

        return (

            f"**{name}**, you unequipped **{item}**.\n\n"

            "Hope you won’t need it in the next fight."

        )



    @staticmethod
    def equipment_broken(
        name,
        item
    ):

        return (

            f"**{name}**, your **{item}** finally gave up.\n\n"

            "Time to find a new one...\n"

            "or start punching monsters."

        )



    @staticmethod
    def hunt_cooldown(
        name,
        time
    ):

        return (

            f"**{name}**, give the poor monsters a tiny break...\n\n"

            f"They’ll be back in **{time}**."

        )



    @staticmethod
    def monster_escaped(
        name,
        monster
    ):

        return (

            f"**{name}**, the **{monster}** ran away laughing.\n\n"

            "Better luck next hunt!"

        )



    @staticmethod
    def run_success(name):

        return (

            f"**{name}**, you escaped!\n\n"

            "Your dignity, however, "
            "is still being questioned."

        )



    @staticmethod
    def defeated(name):

        return (

            f"**{name}**, that monster got the better of you.\n\n"

            "Maybe next time try hitting the monster "
            "instead of the air."

        )



    @staticmethod
    def successful_hunt(name):

        return (

            f"**{name}**, monster defeated!\n\n"

            "Your backpack is a little heavier now."

        )



    @staticmethod
    def pvp_victory(name):

        return (

            f"**{name}**, victory!\n\n"

            "Your opponent has been respectfully "
            "turned into free EXP."

        )



    @staticmethod
    def pvp_defeat(name):

        return (

            f"**{name}**, better luck next duel.\n\n"

            "At least your equipment survived...\n"

            "mostly."

        )




    @staticmethod
    def level_up(
        name,
        level
    ):

        return (

            f"**{name}**, congratulations!\n\n"

            f"You’re now **Level {level}**.\n"

            "The monsters are officially concerned."

        )




    @staticmethod
    def rare_drop(
        name,
        item
    ):

        return (

            f"**{name}**, hold on... what’s that glow?\n\n"

            f"You found **{item}**!"

        )



    @staticmethod
    def legendary_drop(
        name,
        item
    ):

        return (

            f"**{name}**, NO WAY!\n\n"

            f"You actually found **{item}**!\n"

            "Maybe buy a lottery ticket too?"

        )



    @staticmethod
    def divine_drop(
        name,
        item
    ):

        return (

            f"**{name}**, THE STARS HAVE ALIGNED!\n\n"

            f"You obtained **{item}**.\n"

            "Don’t let it get rusty."

        )


    @staticmethod
    def coin_flip_start(
        name,
        bet,
        choice
    ):

        return (

            f"🪙 **Coin Flip**\n\n"

            f"**{name}** bet **{bet:,} Crap Cash** "
            f"and chose **{choice}!**\n\n"

        )



    @staticmethod
    def coin_flip_win(
        name,
        result,
        reward
    ):

        return (

            f"Coin landed on **{result}!**\n\n"

            f"🎉 **{name}** won **{reward:,} Crap Cash!**"

        )



    @staticmethod
    def coin_flip_lose(
        name,
        result,
        lost
    ):

        return (

            f"Coin landed on **{result}!**\n\n"

            f"💀 **{name}** lost **{lost:,} Crap Cash.**"

        )



    @staticmethod
    def blackjack_start(
        name,
        bet
    ):

        return (

            f"🃏 **Blackjack**\n\n"

            f"**{name}** bet **{bet:,} Crap Cash**\n\n"

            "The dealer is preparing the cards..."

        )



    @staticmethod
    def blackjack_win(
        name,
        reward
    ):

        return (

            f"🃏 **Blackjack!**\n\n"

            f"🎉 **{name}** won **{reward:,} Crap Cash!**"

        )



    @staticmethod
    def blackjack_lose(
        name,
        lost
    ):

        return (

            f"🃏 **Blackjack**\n\n"

            f"💀 **{name}** lost **{lost:,} Crap Cash.**"

        )



    @staticmethod
    def slots_win(
        name,
        reward
    ):

        return (

            f"🎰 **Slots Jackpot!**\n\n"

            f"🎉 **{name}** won **{reward:,} Crap Cash!**"

        )



    @staticmethod
    def slots_lose(
        name,
        lost
    ):

        return (

            f"🎰 **Slots**\n\n"

            f"💀 **{name}** lost **{lost:,} Crap Cash.**\n\n"

            "The machine was not feeling generous today."

        )



    @staticmethod
    def max_bet():

        return (

            "⚠️ Maximum bet is **250,000 Crap Cash**."

        )