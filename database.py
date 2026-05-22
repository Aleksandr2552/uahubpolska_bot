import aiosqlite

DB_NAME = "database.db"

async def create_db():

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT
            )
            """
        )

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                category TEXT,
                type TEXT,
                text TEXT
            )
            """
        )

        await db.commit()

async def add_user(user_id, username):

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )

        user = await cursor.fetchone()

        if not user:

            await db.execute(
                "INSERT INTO users (user_id, username) VALUES (?, ?)",
                (user_id, username)
            )

            await db.commit()

async def get_stats():

    async with aiosqlite.connect(DB_NAME) as db:

        users = await db.execute("SELECT COUNT(*) FROM users")
        users_count = await users.fetchone()

        ads = await db.execute("SELECT COUNT(*) FROM ads")
        ads_count = await ads.fetchone()

        return users_count[0], ads_count[0]