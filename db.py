import aiosqlite
import asyncio


class Connect:
    def __init__(self, id):
        self.id = id

    async def GetData(self):
        async with aiosqlite.connect('customers.db') as db:
            cursor = await db.cursor()
            await cursor.execute("create table if not exists users (user_id text,checked text,total text,name text)")
            await db.commit()
            await cursor.execute("SELECT * FROM users where (user_id=?)", (self.id,))
            data=await cursor.fetchall()
            await cursor.close()
        return data
    async def Add(self,chekced,total=0,name=None):
        async with aiosqlite.connect('customers.db') as db:
            cursor = await db.cursor()
            await cursor.execute("insert into users (user_id,checked,total,name) values (?,?,?,?) ", (self.id,chekced,total,name))
            await db.commit()
            await cursor.close()
        return 200
    


