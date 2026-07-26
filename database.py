import aiosqlite
import os


DB_NAME = "data/database.db"


async def initialize_database():

    print("Initializing database...")


    os.makedirs(
        "data",
        exist_ok=True
    )


    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("PRAGMA journal_mode=WAL")
        await db.execute("PRAGMA busy_timeout=5000")


        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS players (

                user_id INTEGER PRIMARY KEY,

                username TEXT NOT NULL,

                coins INTEGER DEFAULT 1200,

                level INTEGER DEFAULT 1,

                experience INTEGER DEFAULT 0,

                hp INTEGER DEFAULT 100,

                wins INTEGER DEFAULT 0,

                losses INTEGER DEFAULT 0,

                surrenders INTEGER DEFAULT 0,
                
                afk_losses INTEGER DEFAULT 0,
                
                lootboxes INTEGER DEFAULT 0,

                daily_streak INTEGER DEFAULT 0,

                last_daily TEXT,

                rank TEXT DEFAULT '🥉 Bronze',
                
                stars INTEGER DEFAULT 0,
                
                battle_cooldown TEXT,
                
                battle_result TEXT
            )
            """
        )



        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                item_name TEXT NOT NULL,

                amount INTEGER DEFAULT 1,

                UNIQUE(user_id, item_name)
            )
            """
        )


        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS equipment (

                user_id INTEGER PRIMARY KEY,

                weapon TEXT DEFAULT NULL,

                armor TEXT DEFAULT NULL,

                weapon_durability INTEGER DEFAULT 100,

                armor_durability INTEGER DEFAULT 100

            )
            """
        )


        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                sender_id INTEGER,

                receiver_id INTEGER,

                amount INTEGER,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
            """
        )


        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS shop_stock (

                item_name TEXT PRIMARY KEY,

                stock INTEGER NOT NULL,

                price INTEGER NOT NULL,

                refreshed_at INTEGER NOT NULL

            )
            """
        )

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS shop_timer (

                id INTEGER PRIMARY KEY,

                last_refresh TEXT NOT NULL

            )
            """
        )


        await db.commit()



    print("Database initialized successfully.")