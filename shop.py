import random
import time
import aiosqlite

from datetime import datetime, timedelta
from utils.items import (
    ITEMS,
    SHOP_CHANCE,
    SHOP_STOCK
)


DB_NAME = "data/database.db"


async def refresh_shop():

    current_time = int(time.time())

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            "DELETE FROM shop_stock"
        )


        for item_name, item in ITEMS.items():

            rarity = item["rarity"]

            chance = SHOP_CHANCE.get(
                rarity,
                0
            )


            roll = random.randint(
                1,
                100
            )


            if roll <= chance:

                stock_range = SHOP_STOCK.get(
                    rarity,
                    (1, 1)
                )


                stock = random.randint(
                    stock_range[0],
                    stock_range[1]
                )


                await db.execute(
                    """
                    INSERT INTO shop_stock
                    (
                        item_name,
                        stock,
                        price,
                        refreshed_at
                    )

                    VALUES (?, ?, ?, ?)
                    """,

                    (
                        item_name,
                        stock,
                        item["price"],
                        current_time
                    )
                )


        await db.commit()

        await db.execute(
            """
            INSERT OR REPLACE INTO shop_timer
            (
                id,
                last_refresh
            )
            VALUES (?, ?)
            """,
            (
                1,
                datetime.now().isoformat()
            )
        )


        await db.commit()