RANKS = [

    "🥉 Bronze",

    "🥈 Silver",

    "🥇 Gold",

    "💎 Platinum",

    "👑 Diamond",

    "🎖️ Master",

    "🌈 Mythic",

    "💩 POO Legendary"

]


MAX_STARS = 5


def add_star(rank, stars):

    old_rank = rank

    stars += 1

    promoted = False


    if stars >= MAX_STARS:

        stars = 0

        index = RANKS.index(rank)

        if index < len(RANKS) - 1:

            rank = RANKS[index + 1]

            promoted = True


    return rank, stars, promoted, old_rank


def remove_star(rank, stars):

    demoted = False
    old_rank = rank

    if stars > 0:

        stars -= 1

    else:

        index = RANKS.index(rank)

        if index > 0:

            rank = RANKS[index - 1]
            stars = 4
            demoted = True

    return rank, stars, demoted, old_rank