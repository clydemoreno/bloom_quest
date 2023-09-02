import asyncio
import aiomysql

async def main():
    # Connection parameters
    db_params = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "mysecretpassword",
        "db": "mydb",
    }

    # Establishing an asynchronous connection
    async with aiomysql.connect(**db_params) as conn:
        async with conn.cursor() as cur:
            # Example query execution
            await cur.execute("SELECT * FROM ORDERS")
            result = await cur.fetchall()
            print(result)

# Running the asyncio event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
