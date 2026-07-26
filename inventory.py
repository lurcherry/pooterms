import aiosqlite

DB_PATH = "data/database.db"


async def add_inventory_item(
    user_id,
    item_name,
    amount=1
):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT amount
            FROM inventory
            WHERE user_id = ?
            AND item_name = ?
            """,
            (
                user_id,
                item_name
            )
        )

        item = await cursor.fetchone()

        if item:

            await db.execute(
                """
                UPDATE inventory
                SET amount = amount + ?
                WHERE user_id = ?
                AND item_name = ?
                """,
                (
                    amount,
                    user_id,
                    item_name
                )
            )

        else:

            await db.execute(
                """
                INSERT INTO inventory
                (
                    user_id,
                    item_name,
                    amount
                )
                VALUES (?, ?, ?)
                """,
                (
                    user_id,
                    item_name,
                    amount
                )
            )

        await db.commit()