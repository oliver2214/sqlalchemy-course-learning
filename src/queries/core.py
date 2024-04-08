from sqlalchemy import insert, text
from database import sync_engine, async_engine
from models import metadata_obj
from models import workers_table


def get_sync_123():
    with sync_engine.connect() as conn:
        res = conn.execute(text("SELECT 1,2,3"))
        print(f"{res.first()=}")
        conn.commit()


async def get_async_123():
    async with async_engine.connect() as conn:
        res = await conn.execute(text("SELECT 1,2,3"))
        print(f"{res.first()=}")


def create_tables():
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)


def insert_data():
    with sync_engine.connect() as conn:
        stmt = insert(workers_table).values(
            [
                {"username": "Aydar"},
                {"username": "Dima"}
            ]
        )
        conn.execute(stmt)
        conn.commit()
