import aiomysql

class OrderRepository:
    def __init__(self, db_params):
        self.db_params = db_params

    async def insert_orders(self, orders):
        async with aiomysql.create_pool(**self.db_params, minsize=5, maxsize=10) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    insert_sql = "INSERT INTO ORDERS (Name) VALUES (%s)"
                    await cursor.executemany(insert_sql, orders)
                    await conn.commit()

    async def select_orders_with_paging(self, page_size, page_number):
        async with aiomysql.create_pool(**self.db_params, minsize=5, maxsize=10) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    offset = (page_number - 1) * page_size
                    select_sql = "SELECT ID, Name FROM ORDERS LIMIT %s OFFSET %s"
                    await cursor.execute(select_sql, (page_size, offset))
                    orders = await cursor.fetchall()
        return orders
    
    async def get_order_by_id(self, order_id):
        async with aiomysql.create_pool(**self.db_params, minsize=5, maxsize=10) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    select_sql = "SELECT ID, Name FROM ORDERS WHERE ID = %s"
                    await cursor.execute(select_sql, (order_id,))
                    order = await cursor.fetchone()
        return order

    async def get_all_orders(self):
        async with aiomysql.create_pool(**self.db_params, minsize=5, maxsize=10) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    select_sql = "SELECT ID, Name FROM ORDERS"
                    await cursor.execute(select_sql)
                    orders = await cursor.fetchall()
        return orders
    
    async def count_records(self):
        async with aiomysql.create_pool(**self.db_params, minsize=5, maxsize=10) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    count_sql = "SELECT COUNT(*) FROM ORDERS"
                    await cursor.execute(count_sql)
                    total_records = (await cursor.fetchone())[0]
        return total_records
