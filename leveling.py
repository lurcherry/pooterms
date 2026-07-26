import aiosqlite

DB_PATH = "data/database.db"


def calculate_level(exp):

    level = 1
    required = 100

    while exp >= required:
        exp -= required
        level += 1
        required = level * 100

    return level, exp


async def add_exp(user_id, amount):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT level, experience
            FROM players
            WHERE user_id = ?
            """,
            (user_id,)
        )

        player = await cursor.fetchone()

        if player is None:
            return

        level, exp = player

        exp += amount

        while exp >= level * 100:
            exp -= level * 100
            level += 1

        await db.execute(
            """
            UPDATE players
            SET level = ?,
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